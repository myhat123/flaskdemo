from ..dbwork import sqldb
from .. import utils
from decimal import Decimal
from flask import render_template
from flask_login import login_required

from . import main

@main.route('/show_rpt_sum_apart/<tran_date>')
@login_required #强制登录
def show_rpt_sum_apart(tran_date: str):
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

