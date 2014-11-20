import pygtk
pygtk.require('2.0')
import gtk

import gobject
import sys
#import glob
#import math
import os


#if not sys.platform.startswith('win'):
#    HOME = os.environ.get('HOME')
#else:
#    HOME = os.environ.get('PYMOL_PATH')
#    

SequenceTest = "MGPPSSSGFYVSRAVALLLAGLVAALLLALAVLAALYGHCERVPPSELPGLRDLEAESSPPLRQKPTPTPKPSSARELAVTTTPSNWRPPGPWDQLRLPPWLVPLHYDLELWPQLRPDELPAGSLPFTGRVNITVRCTVATSRLLLHSLFQDCERAEVRGPLSPGTGNATVGRVPVDDVWFALDTEYMVLELSEPLKPGSSYELQLSFSGLVKEDLREGLFLNVYTDQGERRALLASQLEPTFARYVFPCFDEPALKATFNITMIHHPSYVALSNMPKLGQSEKEDVNGSKWTVTTFSTTPHMPTYLVAFVICDYDHVNRTERGKEIRIWARKDAIANGSADFALNITGPIFSFLEDLFNISYSLPKTDIIALPSFDNHAMENWGLMIFDESGLLLEPKDQLTEKKTLISYVVSHEIGHQWFGNLVTMNWWNNIWLNEGFASYFEFEVINYFNPKLPRNEIFFSNILHNILREDHALVTRAVAMKVENFKTSEIQELFDIFTYSKGASMARMLSCFLNEHLFVSALKSYLKTFSYSNAEQDDLWRHFQMAIDDQSTVILPATIKNIMDSWTHQSGFPVITLNVSTGVMKQEPFYLENIKNRTLLTSNDTWIVPILWIKNGTTQPLVWLDQSSKVFPEMQVSDSDHDWVILNLNMTGYYRVNYDKLGWKKLNQQLEKDPKAIPVIHRLQLIDDAFSLSKNNYIEIETALELTKYLAEEDEIIVWHTVLVNLVTRDLVSEVNIYDIYSLLKRYLLKRLNLIWNIYSTIIRENVLALQDDYLALISLEKLFVTACWLGLEDCLQLSKELFAKWVDHPENEIPYPIKDVVLCYGIALGSDKEWDILLNTYTNTTNKEEKIQLAYAMSCSKDPWILNRYMEYAISTSPFTSNETNIIEVVASSEVGRYVAKDFLVNNWQAVSKRYGTQSLINLIYTIGRTVTTDLQIVELQQFFSNMLEEHQRIRVHANLQTIKNENLKNKKLSARIAAWLRRNT"

ResProp = {'A':['Ala','HID','A'],
           'R':['Arg','POL','B'],
           'N':['Asn','POL','B'],
           'D':['Asp','POL','B'],
           'C':['Cys','HID','A'],
           'E':['Glu','POL','B'],
           'Q':['Gln','POL','B'],
           'G':['Gly','HID','A'],
           'H':['His','POL','B'],
           'I':['Ile','HID','A'],
           'L':['Leu','HID','A'],
           'K':['Lys','POL','B'],
           'M':['Met','HID','A'],
           'F':['Phe','POL','B'],
           'P':['Pro','HID','A'],
           'S':['Ser','POL','B'],
           'T':['Thr','POL','B'],
           'W':['Trp','POL','B'],
           'Y':['Tyr','POL','B'],
           'V':['Val','HID','A']}

def SequenceCount (sequence = "RPPGPWDQLRLPPWLVPLHYDL"):
    """ Function doc """
    HID = 0
    POL = 0
    for i in sequence:
        print i, ResProp[i]
        if ResProp[i][1] == "HID":
            HID = HID +1
        else:
            POL = POL +1
    print "POL", POL
    print "HID", HID
    
class MastersMain:
    """ Class doc """

    def testGTKMatplotLib(self, button):
        """ Function doc """
        import gtk
        from matplotlib.figure import Figure
        from numpy import arange, sin, pi

        # uncomment to select /GTK/GTKAgg/GTKCairo
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

        box = self.builder.get_object('vbox4')
        self.graph = box

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        #t = arange(0.0,3.0,0.01)
        #s = sin(2*pi*t)
        t = range(0, 10)
        s = range(0, 10)

        t = [0,
             5,
             10,
             15,
             20,
             25,
             30,
             35,
             40,
             45,
             50,
             55,
             60,
             65,
             70,
             75,
             80,
             85,
             90,
             95,
             100,
             105,
             110,
             115,
             120,
             125,
             130,
             135,
             140,
             145,
             150,
             155,
             160,
             165,
             170,
             175,
             180,
             185,
             190,
             195,
             200]

        s = [-913.53086808,
             -1978.05074306,
             -2218.21815405,
             -2333.01919415,
             -2391.82858579,
             -2435.17776079,
             -2486.44564867,
             -2543.07423428,
             -2571.71716511,
             -2598.62940311,
             -2616.98004127,
             -2631.60794731,
             -2648.00535887,
             -2661.72725012,
             -2675.65233140,
             -2686.34375946,
             -2696.94907090,
             -2708.65130605,
             -2718.73853503,
             -2726.36193409,
             -2732.59504750,
             -2737.83623730,
             -2742.33435229,
             -2745.28712806,
             -2748.82036113,
             -2752.12502818,
             -2754.57566090,
             -2756.97531091,
             -2758.83136980,
             -2760.53521449,
             -2762.79017667,
             -2764.47319544,
             -2765.99011566,
             -2767.77186148,
             -2770.20329165,
             -2772.66204338,
             -2775.05818125,
             -2776.97966619,
             -2779.02106271,
             -2781.43441141,
             -2783.70324049]

        a.plot(t, s, 'ko', t, s, 'k')
        #a.plot(x, y, 'ko',x, y,'k')
        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        self.graph.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, self.graph)
        self.graph.pack_end(toolbar, False, False)
        self.graph.show_all()
        # gtk.main()




    def on_toolbutton_NewProject_clicked(self, button):
        """ Function doc """

        
        print 'New Project'
        for i in ResProp:
            print i ,ResProp[i][0], ResProp[i][1]

        
        SequenceCount()
        
    def __init__(self):
        self.builder = gtk.Builder()                                     
        self.builder.add_from_file("MastersMainWindow.glade")                     
                                                             
        self.win = self.builder.get_object("window1")                        
        self.builder.connect_signals(self)
        self.win.show()                                                  
    
    def run(self):
        gtk.main()                   

masters = MastersMain()
#import sys
#if len(sys.argv) > 1:
#    gtkdynamo.project.load_coordinate_file_as_new_system(sys.argv[1])
#    gtkdynamo.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')
#
masters.run()
