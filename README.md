# Streamlit_Projet - M1 EFREI PARIS

## But de ce projet : 
je souhaite étudier les données que l'on détient uniquement sur le cas des valeurs foncières non renseignées.

## Preprocessing
J'ai donc gardé toutes les lignes où cette valeur est nulle à l'aide d'un masque avec une fonction :
```ps
def use_mask(mask_value, dataset, column):
    if mask_value == True :
        mask = dataset[f'{column}'].isnull() == mask_value
    return dataset
```
A partir de là, l'idée est de mesurer pour différents critères le nombre de données restantes et le pourcentage vis-à-vis du dataset épuré :
```ps
def get_feedback_nv(dataframe, colonne):
    col_nv = dataframe[f'{colonne}'].value_counts()
    col_rate_nv = round(col_nv*100/len(dataframe[f'{colonne}']))
    
    col_nv = col_nv.rename('nombre de biens sans prix',axis=0)
    col_rate_nv = col_rate_nv.rename('pourcentage',axis=0)

    analysis_col_nv = pd.concat([col_nv, col_rate_nv], axis=1)
    return analysis_col_nv.head(10)
```
Les coordonnées géographiques n'étant utilisées que pour la carte, les valeurs manquantes sont retirées.

## Sidebar et carte

Afficher à partir d'une checkbox, elle donne accès aux filtres interagissant sur la carte sous forme d'un formulaire.
La date sous forme de selection sur calendrier (début et fin)
```ps
start_date = st.sidebar.date_input('Choisir une date de début', debut)
end_date = st.sidebar.date_input('Choisir une date de fin', fin)
```
La localisation par département et par commune avec une zone pour taper du texte
```ps
option_dep = st.sidebar.text_input("choisir un code département",key=("dep"))
option_com = st.sidebar.text_input("Choisir une commune",key=("com"))
```
Le type de biens par selection multiple organisé en liste
```ps
 option_type = st.sidebar.multiselect("Choisir le type de bien",
                                           df_nv['type_local'].unique(),
                                           key="type")
```
Le nombre de pièces qui ne s'affiche que lorsqu'on selectionne un type de logement
Ce filtre est sous la forme d'un slider à 2 variables
```ps
if any(e in ['Appartement','Maison'] for e in option_type):
            surface_min, surface_max = st.sidebar.slider('Choisir un nombre de pièces principales (logement)',
                                                     int(df_nv['nombre_pieces_principales'].min()),
                                                     int(df_nv['nombre_pieces_principales'].max()),
                                                     (int(df_nv['nombre_pieces_principales'].min()),
                                                     int(df_nv['nombre_pieces_principales'].max())),
                                                     1,
                                                     key='rooms')
```
Chaque filtre (excepté nmb de pièces) détient une condition qui affiche le filtre en cours, ou une erreur si nécessaire au droit de la carte.

Les filtres sont ensuite utiliser comme inputs pour faire des masques qui modifient l'affichage de la carte.

## Graphiques

Les graphiques sont dans la continuité de l'étude et permettent de visualiser où, quand, quels types de biens sont les plus concernées par les prix manquants.
Pour ce faire, l'histogramme et le camembert sont les plus adaptés


histogramme intégré streamlit
```ps
st.bar_chart(date_nv['pourcentage'].head(5))
```
C'est le plus simple à mettre en place et est interactif

histogramme seaborn
```ps
sns.set_theme(style="whitegrid")
fig2,ax2 = plt.subplots()
ax2 = sns.barplot(x=type_nv.index, y=type_nv['pourcentage'], data = type_nv)
st.pyplot(fig2)
```

camember matplotlib
ici le camembert nous montre pour chaque type de local sa proportion par prix manquants.
Nous avons entre 0 et 2% des valeurs manquantes par type sur le dataset total, et ce visuel nous donne la part de chacun sur ce sous-total.
```ps
type2 = round((df_nv['type_local'].value_counts()/df['type_local'].value_counts()),3)*100
        fig1,ax1 = plt.subplots()
        ax1.pie(type2, labels=type_nv.index, autopct='%1.1f%%')
        ax1.axis('equal')
        st.pyplot(fig1)
```
Le choix de visualiser l'histogramme ou le camembert des types de locaux se fait via une selectbox.

Pour ces graphiques, le résultat est commenté et il y a également un compteur qui indique le pourcentage de valeurs manquantes pour la catégorie elle-même. Ex : 60% dans le cas des types de locaux.
```ps
st.write("<font color='red'>Valeurs manquantes dans la colonne 'type_local' : </font>",
         100*round(1-len(drop_na(df_nv,'type_local'))/len(df_nv.index),1),
         "<font color='red'>%</font>", unsafe_allow_html=True)
```

## Autres

Un fichier Runtime.txt se met à jour à chaque execution car il existe une fonction main()
avec un décorateur qui enregistre le temps d'exécution et le timestamp à la suite du fichier.
```ps
def exeTime(func): 
    
    def countTime():
        print('---Buffering---')
        start = time.time()   
        func()
        time.sleep(1)
        end = time.time() - 1 #évite d'avoir un temps de 0.0
        diff = round(end-start,4)
        stp = datetime.datetime.now().timestamp()
        
        
        msg = f"Le temps d'execution de {func} est de {diff} secondes. Timestamp : {stp}"
        print(msg)
        file1 = open("RunTime.txt","a") #fichier RunTime.txt qui stocke les temps d'exé
        file1.write(msg + "\n")
        file1.close() 
    return countTime
```

```ps
@exeTime
def main():
[...]
if __name__ == "__main__":
    main()
```

Les chargements et traitements de données sont quasiement tous organisés sous forme de fonction
avec la mention @st.cache pour optimiser les temps de rechargement
