from decimal import Decimal

class Filters():
    def init_app(self, app):
        @app.template_filter('filter')
        def num_filter(x: Decimal):
            s = float(x)
            if s > 10000:
                s = s / 10000
                return str(round(s, 2)) + '万元'

            else:
                return str(s) + '元'