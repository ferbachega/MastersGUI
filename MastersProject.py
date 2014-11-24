# System
import sys
import os
import pango


PROJECT = {
            'teste com promotor'   : ['/home/fernando/Documents/masterGUI/promotor.project',           'Sat Nov 22 12:54:04 2014', 'Mon Nov 24 13:54:04 2014', '7' ]                   ,
            'proteina hipotetica'  : ['/home/fernando/Documents/masterGUI/ReceptorDeMembrana.project', 'Sat Nov 22 12:54:04 2014', 'Mon Nov 24 13:54:04 2014', '10']                   ,
            'projeto teste'        : ['/home/fernando/Documents/masterGUI/ReceptorDeMembrana.project', 'Sat Nov 22 12:54:04 2014', 'Mon Nov 24 13:54:04 2014', '10']                   ,
            'Receptor de Membrana' : ['/home/fernando/Documents/masterGUI/ReceptorDeMembrana/ReceptorDeMembrana.project', 'Sat Nov 22 12:54:04 2014', 'Mon Nov 24 13:54:04 2014', '10'],
            'Receptor mutacao'     : ['/home/fernando/Documents/masterGUI/ReceptorMutacao.project', '   Sat Nov 22 12:54:04 2014', 'Mon Nov 24 13:54:04 2014', '15']                   ,
            'proteina alvo'        : ['/home/fernando/Documents/masterGUI/ReceptorDeMembrana.project', 'Sat Nov 22 12:54:04 2014', 'Mon Nov 24 13:54:04 2014', '10'] 
            }


class ProjectsControl:
    """ Class doc """
    
    def __init__ (self, builder = None, teste = False):
        """ Class initialiser """
        self.home     = os.environ.get('HOME')
        self.builder  = builder
        self.projects = {}
        
        if teste == True:
            self.projects = PROJECT
        
        print self.projects
        
    def LoadProjectsFromHistory (self):
        """ Function doc """
        try:
            ProjectsFromHistoryFile = open(self.home + '/.MasterProjects', 'r')
            for line in ProjectsFromHistoryFile:
                line2 = line.split('|')
                self.projects[line2[0]] = line2[1:]
        except:
            #creating a new ProjectsFromHistoryFile
            ProjectsFromHistoryFile = open(self.home + '/.MasterProjects', 'a')
        for i in self.projects:
            print i, self.projects[i]

    def AddHistoryToTreeview (self, liststore=None):
        model = self.builder.get_object('liststore2')  # @+
        model.clear()
        n = 0
        for i in self.projects:
            #cell = self.builder.get_object('cellrenderertext1')
            #cell.props.weight = pango.WEIGHT_BOLD
            data = [False, i ,  self.projects[i][2], self.projects[i][3]]
            print i
            model.append(data)
            n = n + 1

        
class MasterProject:
    """ Class doc """
    def __init__ (self):
        """ Class initialiser """
        self.sequence = 'MHVTQSSSAITPGQTAELYPGDIKSVLLTAEQIQARIAELGEQIGNDYRELSATTGQ'
   
        self.history={
                     1:['Monte Carlos sim.','Sat Nov 22 12:54:04 2014', 'teste do mastrer'     ,'34523.8976 KJ', {}],
                     2:['Monte Carlos sim.','Sun Nov 23 13:50:10 2014', 'teste do mastrer2'    ,'35523.8976 KJ', {}],
                     3:['Monte Carlos sim.','Sun Nov 23 14:34:04 2014', 'teste do mastrer3'    ,'35723.8976 KJ', {}],
                     4:['Monte Carlos sim.','Sun Nov 23 15:00:07 2014', 'repetindo teste 2'    ,'35783.8976 KJ', {}],
                     5:['Monte Carlos sim.','Mon Nov 24 18:54:04 2014', 'Troca de param. tese4','35789.8976 KJ', {}],
                    }
        
project = ProjectsControl(teste= True)
#project.LoadProjectsFromHistory()
