import pandas
import settings
from sql_control import SqlControl


class PlotFigure(SqlControl):

    def __init__(self):
        figure_dir = settings.base_dir() + "/figure"
        SqlControl.open_commodity_conn(self)




        SqlControl.close_commodity_conn(self)

    def get_spot_name(self):
        sql = "SELECT * FROM "