from download import DataDownloader
from matplotlib import pyplot as plt
import os, argparse


def count_accidents_by_year(region,data_by_region,date): 
    if (date == '2016'):
        try:
            if len(data_by_region[region][0]) == 0:
                data_by_region[region][0] = 1
        except:
            data_by_region[region][0] += 1
    elif (date == '2017'):
        try:
            if len(data_by_region[region][1]) == 0:
                data_by_region[region][1] = 1
        except:
            data_by_region[region][1] += 1
    elif (date == '2018'):
        try:
            if len(data_by_region[region][2]) == 0:
                data_by_region[region][2] = 1
        except:
            data_by_region[region][2] += 1
    elif (date == '2019'):
        try:
            if len(data_by_region[region][3]) == 0:
                data_by_region[region][3] = 1
        except:
            data_by_region[region][3] += 1
    elif (date == '2020'):
        try:
            if len(data_by_region[region][4]) == 0:
                data_by_region[region][4] = 1
        except:
            data_by_region[region][4] += 1


def plot_stat(data_source, fig_location = None, show_figure = False):
    data_by_region = {}
    years = ['2016','2017','2018','2019','2020']
    regions = list(set(data_source[1][64]))
    for i in range(len(regions)):
        data_by_region[regions[i]] = [[] for _ in range(5)] 
    for i in range(len(data_source[1][0])):
        region = data_source[1][64][i]
        date = data_source[1][3][i].split('-')[0]
        if region in data_by_region:
            count_accidents_by_year(region,data_by_region,date)
            
    
    plt.figure(figsize=(8.27,11.69))
    plt.suptitle("Počet nehôd v českých krajoch počas vybraných rokov",fontsize=12)
    for i in range(len(data_by_region[regions[0]])):
        list_of_values = {}
        for j in range(len(data_by_region)):
            list_of_values[regions[j]] = data_by_region[regions[j]][i]
        sort_orders = sorted(list_of_values.items(), key=lambda x: x[1], reverse=True)
        ax = plt.subplot(5,1,i+1)
        plt.ylabel("Počet nehôd",fontsize=7)
        plt.title(years[i])
        bar1 = plt.bar(list_of_values.keys(),list_of_values.values(),width=0.6,color='fuchsia')
        for i in range(len(sort_orders)):
            list_of_values[sort_orders[i][0]] = i+1
        for rect in bar1:
            height = rect.get_height()
            for i in range(len(sort_orders)):
                if sort_orders[i][1] == height:
                    order = list_of_values[sort_orders[i][0]]
            plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(order), ha='center', va='bottom')
        plt.grid(color='#95a5a6', linestyle='-', linewidth=1, axis='y', alpha=0.3)
        plt.subplots_adjust(hspace=0.7, top=0.91, bottom=0.05)
        plt.yticks([0,5000, 10000, 15000,20000, 25000])
        plt.ylim(top=30000)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    if fig_location is not None:
        location = os.path.dirname(fig_location)
        filename = os.path.basename(fig_location)
        if os.path.isdir(location):
            plt.savefig(os.path.join(location,filename),dpi=600)
        else:
            os.mkdir(location)
            plt.savefig(os.path.join(location,filename),dpi=600)

    if show_figure is True:
        plt.show()
       

if __name__ == "__main__":
    argsparser = argparse.ArgumentParser(description="")
    argsparser.add_argument("--fig_location", nargs=1)
    argsparser.add_argument("--show_figure", nargs=1)

    args = argsparser.parse_args()
    show_figure = False
    fig_location = None

    try:
        if args.show_figure[0] == 'True':
            show_figure = True
        else:
            show_figure = False
    except:
        show_figure = False

    if args.fig_location is not None:
        fig_location = args.fig_location[0]
    else:
        fig_location = None
    
    data_source = DataDownloader().get_list()
    plot_stat(data_source,fig_location=fig_location,show_figure=show_figure)