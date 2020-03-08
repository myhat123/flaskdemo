from ..dbwork import sqldb
from .. import utils
from .. import settings
from decimal import Decimal
from flask import render_template
from flask_login import login_required

from . import main

@main.route('/show_rpt_sum_apart/<tran_date>')
@login_required
def show_rpt_sum_apart(tran_date: str):
    '''展示首页'''

    q = sqldb.SQLDB()
    inner = q.get_time_range_dtl(tran_date, '1')
    outer = q.get_time_range_dtl(tran_date, '2')

    gs_time = [x['time'].strftime('%H:%M') for x in inner]
    # gs_amt_in = [float(x['amt']) for x in inner]
    # gs_amt_out = [float(x['amt']) for x in outer]

    gs_sum_in = utils.get_sum([x['amt'] for x in inner])
    gs_sum_out = utils.get_sum([x['amt'] for x in outer])


    amt_sum_in = q.get_details_amt(tran_date, '1')
    amt_sum_out = q.get_details_amt(tran_date, '2')

    total_in = sum([x['amt'] for x in amt_sum_in])
    total_out = sum([x['amt'] for x in amt_sum_out])

    members_in = q.get_members_rank(tran_date, '1')[:10]
    members_out = q.get_members_rank(tran_date, '2')[:10]

    inner_apart = q.get_time_range_dtl_apart(tran_date, '1')
    outer_apart = q.get_time_range_dtl_apart(tran_date, '2')

    gs_amt_in = [{'y': float(x['amt']), 'details': x['details']} for x in utils.merge_details(inner, inner_apart)]
    gs_amt_out = [{'y': float(x['amt']), 'details': x['details']} for x in utils.merge_details(outer, outer_apart)]

    return render_template('main/index.html', 
        total_in=total_in,
        total_out=total_out,
        amt_sum_in=amt_sum_in,
        amt_sum_out=amt_sum_out,
        gs_time=gs_time, 
        gs_amt_in=gs_amt_in,
        gs_amt_out=gs_amt_out, 
        gs_sum_in=gs_sum_in,
        gs_sum_out=gs_sum_out,
        members_in=members_in,
        members_out=members_out
    )

@main.route("/show_access_log")
@login_required
def show_access_log():
    '''显示归属网点'''

    q = sqldb.SQLDB()
    total = q.get_access_cnt('20200212', '20200216')
    for x in total:
        x['color'] = utils.get_access_color(x['cnt'])

    q.close()

    return render_template('main/show_access_log.html',
        access_color=settings.ACCESS_COLOR,
        total=total,
    )

@main.route("/show_access_details")
@login_required
def show_access_details():
    '''显示网点访问日志'''

    q = sqldb.SQLDB()

    results = q.get_access_log('20200216')

    q.close()

    return render_template('main/show_access_details.html',
        results=results
    )