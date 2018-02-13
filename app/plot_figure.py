import pandas
import settings
from sql_control import SqlControl
import pygal

class PlotFigure(SqlControl):

    def __init__(self):
        print("Figure plotting, please wait.")
        SqlControl.__init__(self)
        self.figure_dir = settings.base_dir() + "/figure"   #figure document location
        SqlControl.open_commodity_conn(self)
        spot_tb_name = "spot"# spot table name         # the commodity table name
        spot = self.get_spot_name(spot_tb_name)                         # to get the commodity spot name
        self.plot_figure(spot)                              # use pygal to plot all the spot
        SqlControl.close_commodity_conn(self)
        print("Figures have been plotted.")

    def get_spot_name(self, spot_tb_name):
        sql = "SELECT * FROM {0}".format(spot_tb_name)
        spot = pandas.read_sql(sql, self.com_conn)
        return spot

    def plot_figure(self, spot):
        spot_index = spot.dtypes.index
        spot_date = spot.loc[:, spot_index[0]]  # the datetime
        spot_date = list(spot_date)
        spot_date = list(map(lambda x: int(x), spot_date))   # date in int format list
        for ind in range(len(spot_index)):          # due to the first one is the date in string, it has to be bypass.
            if ind == 0:
                continue
            spot_df = spot.loc[:, spot_index[ind]]   # each spot data
            spot_df = list(spot_df)             # spot price in list
            # plot
            fig = pygal.Line()
            fig.title = spot_index[ind]
            fig.x_labels = spot_date
            fig.add(spot_index[ind], list(spot_df))
            #save the figure to png document in "/figure" dir
            fig_path = self.figure_dir + "/{0}.png".format(spot_index[ind])
            fig.render_to_png(fig_path)

if __name__ == "__main__":
    p = PlotFigure()