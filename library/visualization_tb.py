import os
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np 
from wordcloud import WordCloud


class Gestor_apariencia:

    def set_theme(self, option):
        plt.style.use('seaborn')
        if option == 'a':
            sns.set(rc={'axes.facecolor':'cadetblue', 
                        'figure.facecolor':'cadetblue', 
                        'grid.color': 'turquoise', 
                        'grid.linestyle': ':', 
                        'xtick.color': 'white', 
                        'ytick.color': 'white', 
                        'text.color': 'white', 
                        'axes.labelsize': 10, 
                        'axes.titlesize': 15, 
                        'font.size':10,
                        'xtick.labelsize': 10,
                        'ytick.labelsize': 10})
        if option == 'b':
            sns.set(rc={'axes.facecolor':'indianred', 
                        'figure.facecolor':'indianred', 
                        'grid.color': 'lightpink', 
                        'grid.linestyle': ':', 
                        'xtick.color': 'white', 
                        'ytick.color': 'white', 
                        'text.color': 'white', 
                        'axes.labelsize': 10, 
                        'axes.titlesize': 15, 
                        'font.size':10,
                        'xtick.labelsize': 10,
                        'ytick.labelsize': 10})



class Plotter(Gestor_apariencia):

    def default_values(self, labelx=None, labely=None, title=None, rotation=None, figsize=(6, 6)):
        fig, ax = plt.subplots(figsize=figsize)
        plt.ylabel(labely, color='white', labelpad=14)
        plt.xlabel(labelx, color='white', labelpad=14)
        plt.title(title, pad=35)
        plt.xticks(size=15, rotation=rotation)
        plt.yticks(size=15)
        sns.despine(right=False, top=False)
        return fig, ax


    def visualizar(self, kind, df=None, x=None, y=None, ax=None, bins=None, hue=None, external_xlabel=None, external_ylabel=None, color='white', label=None):
        if kind == 'lm':
            h = sns.lmplot(x=x, y=y, data=df, line_kws={'color': color}, scatter_kws={'color': color}, x_bins=bins, hue=hue)
            h.set_axis_labels(external_xlabel, external_ylabel, color=color)
            sns.despine(right=False, top=False)
            return h
        elif kind == 'line':
            sns.lineplot(data=df, x=x, y=y, color=color, ax=ax, hue=hue)
        elif kind == 'joint':
            h = sns.jointplot(x=x, y=y, data=df, color=color, ax=ax, hue=hue)
            h.set_axis_labels(external_xlabel, external_ylabel, color=color)
            return h
        elif kind == 'hist':
            if not bins:
                sns.histplot(x=x, data=df, color=color, ax=ax, hue=hue, label=label)
                if label:
                    ax.legend(prop={'size': 12}) 
            else: 
                sns.histplot(x=x, data=df, color=color, ax=ax, bins=bins, hue=hue, label=label)
                if label:
                    ax.legend(prop={'size': 12}) 
        elif kind == 'count':
            sns.countplot(x=x, data=df, color=color, alpha=.8, ax=ax, hue=hue)
        elif kind == 'bar':
            sns.barplot(x=x, y=y, color=color, alpha=.8, ax=ax, hue=hue)
        elif kind == 'dist':
            sns.distplot(x=x, color=color, ax=ax, bins=bins)
        elif kind == 'cat':
            sns.catplot(x=x, y=y, data=df, color=color, ax=ax, hue=hue)
        elif kind == 'scatter':
            sns.scatterplot(x=x, y=y, data=df, color=color, ax=ax, hue=hue)
        elif kind == 'dis':
            sns.displot(x=x, y=y, data=df, color=color, ax=ax, hue=hue)
        elif kind == 'box':
            # self.set_boxplot_lines_colours(ax)
            sns.boxplot(x=x, data=df, color=color, flierprops={'markerfacecolor':'dimgray'} , ax=ax, hue=hue)
            plt.setp(ax.lines, color='dimgray')


    def set_boxplot_lines_colours(self, ax):
        for i in range(6):
            line = ax.lines[i]
            line.set_color('white')
            line.set_mfc('white')
            line.set_mec('white')


    def subplots(self, numerox, numeroy, titulos, sharex=False, sharey=False, label=False):
        fig, ax = plt.subplots(numerox, numeroy, figsize=(7*numeroy, 7*numerox), sharex=sharex, sharey=sharey)
        if numerox == 1:
            for titulo, j in zip(titulos, range(numeroy)):
                ax[j].set_title(titulo, color='white')
                if label:
                    ax[j].legend(prop={'size': 20}) 
        elif numeroy == 1:
            for titulo, i in zip(titulos, range(numerox)):
                ax[i].set_title(titulo, color='white')
                if label:
                    ax[i].legend(prop={'size': 20}) 
        else:
            for list_titulos,  i in zip(titulos, range(numerox)):
                for j, titulo in zip(range(numeroy), list_titulos):
                    ax[i,j].set_title(titulo, color='white')
                    if label:
                        ax[i, j].legend(prop={'size': 20}) 
        sns.despine(right=False, top=False)
        return fig, ax


    def visualizacion_multiple(self, tipos, ax, xlabels, ylabels, df=None, valoresx=None, valoresy=None, bins=None, hue=None, color='white', label=None):
        try:
            for i, list_xlabels, list_ylabels, list_valorx, list_valory, list_tipo in zip(range(ax.shape[0]), xlabels, ylabels, valoresx, valoresy, tipos):
                for j, xlabel, ylabel, valorx, valory, tipo in zip(range(ax.shape[1]), list_xlabels, list_ylabels, list_valorx, list_valory, list_tipo):
                        self.visualizar(x=valorx, y=valory, df=df, ax=ax[i, j], kind=tipo, bins=bins, hue=hue, color=color, label=label)
                        ax[i,j].set_xlabel(xlabel, color='white')
                        ax[i,j].set_ylabel(ylabel, color='white')
        except (TypeError, IndexError):
            if valoresy:
                for valorx, valory, tipo, i, xlabel, ylabel in zip(valoresx, valoresy, tipos, range(ax.shape[0]), xlabels, ylabels):
                    self.visualizar(x=valorx, y=valory, df=df, ax=ax[i], kind=tipo, bins=bins, hue=hue, color=color, label=label)
                    ax[i].set_xlabel(xlabel, color='white')
                    ax[i].set_ylabel(ylabel, color='white')
            else:
                for valorx, tipo, i, xlabel, ylabel in zip(valoresx, tipos, range(ax.shape[0]), xlabels, ylabels):
                    self.visualizar(x=valorx, df=df, ax=ax[i], kind=tipo, bins=bins, hue=hue, color=color, label=label)
                    ax[i].set_xlabel(xlabel, color='white')
                    ax[i].set_ylabel(ylabel, color='white')


    def guardar_figura(self, fig, nombre, ruta):
        fig.savefig(ruta + os.sep + 'reports' + os.sep + nombre)


    def heatmap(self, df, figsize=(14, 10), rotation=None, annot_size=15, text_size=15):
        fig = plt.figure(figsize=figsize)
        df_corr = df.corr()
        plt.xticks(size=text_size, rotation=rotation)
        plt.yticks(size=text_size, rotation=rotation)
        mask = np.triu(np.ones_like(df_corr, dtype=bool))
        sns.heatmap(df_corr, annot=True, alpha=.9, mask=mask, center=0, fmt='.2f', square=True, annot_kws={"size":annot_size}, cmap="YlGnBu")
        return fig

    def wordcloud(self, lista):
        fig = plt.figure(figsize=(12, 10))
        index = (lista)
        lista_unidos = [word.replace(' ', '_') for word in index]
        text = ' '.join(lista_unidos)
        wordcloud = WordCloud(width = 500, height = 500, max_words = 100000, background_color = 'white').generate(text)
        plt.imshow(wordcloud, interpolation = 'bilinear')
        plt.axis('off')
        plt.margins(x = 0, y = 0)
        return fig


    def pie_chart(self, df, titulo):
        fig, ax = plt.subplots(figsize=(9, 9))
        cmap = plt.get_cmap('Set3')
        colors = [cmap(i) for i in np.linspace(0, 1, 8)]
        patches, texts, pcts = ax.pie(df.values, labels=df.index, autopct='%1.1f%%', colors=colors, textprops={'size': 'x-large'})
        plt.setp(pcts, color='dimgray', fontweight='bold')
        ax.set_title(titulo, fontsize=18)
        return fig


    def plot_multi(self, data, cols=None, spacing=.1, **kwargs):
        """
        Representa en una misma figura todas las columnas con diferentes ejes y.
        """
        from pandas.plotting._matplotlib.style import get_standard_colors

        # Get default color style from pandas - can be changed to any other color list
        if cols is None: cols = data.columns
        if len(cols) == 0: return
        colors = get_standard_colors(num_colors=len(cols))

        # First axis
        ax = data.loc[:, cols[0]].plot(label=cols[0], color=colors[0], **kwargs)
        ax.set_ylabel(ylabel=cols[0])
        lines, labels = ax.get_legend_handles_labels()

        for n in range(1, len(cols)):
            # Multiple y-axes
            ax_new = ax.twinx()
            ax_new.spines['right'].set_position(('axes', 1 + spacing * (n - 1)))
            data.loc[:, cols[n]].plot(ax=ax_new, label=cols[n], color=colors[n % len(colors)], **kwargs)
            ax_new.set_ylabel(ylabel=cols[n])
            
            # Proper legend position
            line, label = ax_new.get_legend_handles_labels()
            lines += line
            labels += label

        ax.legend(lines, labels, loc=0)
        return ax