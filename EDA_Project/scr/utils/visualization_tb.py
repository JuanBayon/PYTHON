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


    def allcolumns_hist_bin5(self, df):
        titulos = [['VALORACIONES DE TMDb', 'CANTIDAD DE VOTOS TMDb', 'AÑO'], 
                    ['PRESUPUESTO', 'RECAUDACIÓN EEUU', 'RECUAUDACIÓN MUNDIAL'], 
                    ['VALORACIONES METACRITIC', 'CANTIDAD VOTOS IMDb', 'VALORACIONES IMDb'],
                    ['VALORACIONES HASTA 18 AÑOS', 'VALORACIONES DE 18 A 30 AÑOS', 'VALORACIONES DE 30 A 45 AÑOS'],
                    ['VALORACIONES MAYORES 45 AÑOS', 'VALORACIONES HOMBRES', 'VOTO HOMBRES HASTA 18 AÑOS'],
                    ['VOTO HOMBRES DE 18 A 30 AÑOS', 'VOTO HOMBRES DE 30 A 45 AÑOS', 'VOTO HOMBRES MAYORES 45 AÑOS'],
                    ['VALORACIONES MUJERES', 'VOTO MUJERES HASTA 18 AÑOS', 'VOTO MUJERES DE 18 A 30 AÑOS'],
                    ['VOTO MUJERES DE 30 A 45 AÑOS', 'VOTO MUJERES MAYORES 45 AÑOS', 'VOTO MUJERES MAYORES 45 AÑOS'],
                    ['VOTO AMERICANOS', 'VOTO NO AMERICANOS', 'VOTO NO AMERICANOS']]
        xlabels = [[None]*3] * 9
        ylabels = [[None]*3] * 9
        valoresx = [['tmdb_ratings', 'tmdb_vote_count', 'year'], 
                    ['budget', 'usa_gross_income', 'worlwide_gross_income'], 
                    ['metascore', 'total_votes', 'imdb_ratings'], 
                    ['allgenders_0age_avg_vote', 'allgenders_18age_avg_vote', 'allgenders_30age_avg_vote'], 
                    ['allgenders_45age_avg_vote', 'males_allages_avg_vote', 'males_0age_avg_vote'], 
                    ['males_18age_avg_vote', 'males_30age_avg_vote', 'males_45age_avg_vote'],
                    ['females_allages_avg_vote', 'females_0age_avg_vote', 'females_18age_avg_vote'], 
                    ['females_30age_avg_vote', 'females_45age_avg_vote', 'females_45age_avg_vote'], 
                    ['us_voters_rating', 'non_us_voters_rating', 'non_us_voters_rating']]
        valoresy = [[None]*3] * 9
        tipos = [['hist']*3] * 9
        
        fig, ax = self.subplots(9, 3, titulos=titulos)
        self.visualizacion_multiple(df=df, valoresx=valoresx, tipos=tipos, ax=ax, valoresy=valoresy, bins=5, xlabels=xlabels, ylabels=ylabels)
        return fig


    def pie_chart(self, df, titulo):
        fig, ax = plt.subplots(figsize=(9, 9))
        cmap = plt.get_cmap('Set3')
        colors = [cmap(i) for i in np.linspace(0, 1, 8)]
        patches, texts, pcts = ax.pie(df.values, labels=df.index, autopct='%1.1f%%', colors=colors, textprops={'size': 'x-large'})
        plt.setp(pcts, color='dimgray', fontweight='bold')
        ax.set_title(titulo, fontsize=18)
        return fig