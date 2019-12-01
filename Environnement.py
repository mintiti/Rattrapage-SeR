# coding=utf-8
# IMPORTS
import numpy as np
import random
from Read_Excel import read_excel_data


class ReseauTelecom:
    """
    Décris l'environnement
    contient Steiner Node, target node et les clients
    contient les coûts de liaison de chaque poste
    contient la fonction qui calcule le cout total de construction

    Attributs :
        - steiners : numpy array d'un nb fixé de couple, décrivant une coordonnée
        - target_nodes : numpy array d'un nb fixé de couple, décrivant une coordonnée
        - clients : numpy array d'un nb fixé de couple, décrivant une coordonnée
    """

    def __init__(self, nb_steiner=6, nb_targetNode=5, nb_clients=8, grid_size=(10, 10)):
        """
        Initialise le Réseau de neurones aléatoirement uniformement sur la grille

        :param nb_steiner: nombre de Steiner node voulus
        :param nb_targetNode: nombre de Target Node voulus
        :param nb_clients: nombre de clients voulus
        :param grid_size: taille de la grille
        :type grid_size: tuple[int,int]
        """

        (x, y) = grid_size
        self.grid_size = grid_size
        self.steiners = [(random.uniform(0, x), random.uniform(0, y)) for i in range(nb_steiner)]
        self.nb_steiner = nb_steiner

        self.target_nodes = [(random.uniform(0, x), random.uniform(0, y)) for i in range(nb_targetNode)]
        self.nb_target_node = nb_targetNode

        self.clients = [(random.uniform(0, x), random.uniform(0, y)) for i in range(nb_clients)]
        self.nb_clients = nb_clients
def dict_to_matrix (matrix,dict):
    (m,n) = matrix.shape
    for i in range(m):
        for j in range(n):
            matrix[i,j] = dict[(i+1,j+1)]
class ReseauTelecomFromExcel :

    def __init__(self, excel):
        # Extract input data from excel file
        self.nb_steiner = read_excel_data(excel,'N')[0]
        self.nb_targetNode = read_excel_data(excel,'M')[0]
        self.nb_client = read_excel_data(excel, 'C')[0]

        # Extract C_cust_target from excel
        dict = read_excel_data(excel, 'CustToTargetAllocCost(hij)')
        self.C_cust_target = np.zeros((self.nb_client, self.nb_targetNode), dtype=int)
        dict_to_matrix(self.C_cust_target,dict)

        # Extract C_target_steiner from excel
        dict = read_excel_data(excel,'TargetToSteinerAllocCost(cjk)')
        self.C_target_steiner = np.zeros((self.nb_targetNode,self.nb_steiner), dtype= int)
        dict_to_matrix(self.C_target_steiner,dict)

        # Extract C_steiner_steiner from excel
        dict = read_excel_data(excel, 'SteinerToSteinerConnctCost(gkm)')
        self.C_steiner_steiner = np.zeros((self.nb_steiner, self.nb_steiner), dtype= int)
        dict_to_matrix(self.C_steiner_steiner,dict)

        #Extract steiner_fixed_cost from excel
        # This time read function return list(int)
        self.steiner_fixed_cost = read_excel_data(excel, 'SteinerFixedCost(fk)')
        self.steiner_capacity = read_excel_data(excel, 'SteinerCapacity(Vk)')
        self.target_capacity = read_excel_data(excel, 'TargetCapicity(Uj)')



if __name__ == '__main__':
    InputData = "InputDataTelecomSmallInstance.xlsx"
    S = ReseauTelecomFromExcel(InputData)
    print(S.C_steiner_steiner)



