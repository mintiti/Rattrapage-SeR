import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from config import cfg

# Constants
SMALL_DATA_INSTANCE = 'InputDataTelecomSmallInstance.xlsx'
LARGE_DATA_INSTANCE = "InputDataTelecomLargeInstance.xlsx"
# Todo : add data instance
# Todo : add best score obtained
# Todo : name based on XXX

class Display :
    def __init__(self,genetic,data_instance):
        """
        Initializes the fig to animate
        genetic should be evaluated at least once
        :param genetic:
        """
        self.data = data_instance
        #Initialize the figure to draw on
        self.fig = plt.figure()

        # Create text ax
        self.text_ax = self.fig.add_subplot(311)
        self.text_ax.set_title('Simulation constants')
        self.text_ax.get_xaxis().set_visible(False)
        self.text_ax.get_yaxis().set_visible(False)
        self._create_text_ax()

        # Create the history of best scores by generation ax
        self.history_ax = self.fig.add_subplot(312)
        self.history_ax.set_xlabel('Generation')
        self.history_ax.plot(range(len(genetic.current_best_list)),[generations_best[1] for generations_best in genetic.current_best_list])

        self.best_score = self.fig.add_subplot(313)
        self.best_score.get_xaxis().set_visible(False)
        self.best_score.get_yaxis().set_visible(False)
        self.best_score.text(0.1,0,"Best score obtained is {0} in {1} generations".format(genetic.current_best[1], genetic.generation_counter))


    def _create_text_ax(self):
        string = None
        if self.data == SMALL_DATA_INSTANCE :
            string = "Data instance : Small\n"
        else :
            string = "Data instance : Large\n"
        for key in cfg.keys():
            string += "{0} : {1}".format(key, cfg[key]) + "\n"
        self.text_ax.text(0.1,0,string)

    def update(self,genetic):
        self.history_ax.plot([i+1 for i in range(len(genetic.current_best_list))] ,[generations_best[1] for generations_best in genetic.current_best_list])

    def save(self,name):
        plt.savefig(name)
        print('saved as ', name )

if __name__ == '__main__':
    from genetic import Genetic
    genetic = Genetic('InputDataTelecomSmallInstance.xlsx')
    genetic.evaluate()
    d= Display(genetic)
    animation.FuncAnimation(d.fig,d.update,frames=genetic)
    plt.show()
    genetic.selection()
    genetic.crossover()
    genetic.mutate()
    genetic.evaluate()
    d.update(genetic)
    animation.FuncAnimation(d.fig, d.update,frames=genetic)



    plt.show()



