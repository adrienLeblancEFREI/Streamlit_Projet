"""
Created on Fri Sep 24 2021

@author: adrien leblanc
"""

# --- IMPORTS ---
import os
import time
import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import sweetviz
#from pandas_profiling import ProfileReport

# --- FONCTIONS ---

## Mesure du temps d'exécution
# le décorateur exeTime servira à mesure le temps d'exé de la page complète

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

## Dataset - chargement
@st.cache(allow_output_mutation=True, 
              suppress_st_warning=True)
def load_dataset(dataset):
    data = pd.read_csv(os.path.abspath(dataset))
    return data

@st.cache(allow_output_mutation=True, 
              suppress_st_warning=True)
def load_dataset_from_url(url):
    data = pd.read_csv(url)
    return data

## Dataset - prétraitement & sélection
# fonction masque comprenant les valeurs nulles
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)    
def use_mask(mask_value, dataset, column):
    if mask_value == True :
        mask = dataset[f'{column}'].isnull() == mask_value
    else :
        mask = dataset[f'{column}'] == mask_value
    dataset = dataset[mask]
    return dataset

# fonction masque , valeur comprise dans
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)    
def use_mask_isin(mask_value, dataset, column):
    mask = dataset[f'{column}'].isin(mask_value)
    dataset = dataset[mask]
    return dataset

# fonctions masque pour la date
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)    
def use_mask_inf(mask_value, dataset, column):
    mask = dataset[f'{column}'] < mask_value
    dataset = dataset[mask]
    return dataset
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)    
def use_mask_sup(mask_value, dataset, column):
    mask = dataset[f'{column}'] > mask_value
    dataset = dataset[mask]
    return dataset

# fonction pour compter les occurences d'une colonne & pourcentage
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)
def get_feedback_nv(dataframe, colonne):
    col_nv = dataframe[f'{colonne}'].value_counts()
    col_rate_nv = round(col_nv*100/len(dataframe[f'{colonne}']))
    
    col_nv = col_nv.rename('nombre de biens sans prix',axis=0)
    col_rate_nv = col_rate_nv.rename('pourcentage',axis=0)

    analysis_col_nv = pd.concat([col_nv, col_rate_nv], axis=1)
    return analysis_col_nv.head(10)

# fonction pour retirer une colonne
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)
def drop_col(df, colonne):
    return df.drop(columns=[f'{colonne}'])
    
#fonction pour retirer les valeurs nulles d'une colonne
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)
def drop_na(df, colonne):
    return df.dropna(subset=[f'{colonne}'])

# fonction format datetime pandas
@st.cache(allow_output_mutation=True,
          suppress_st_warning=True)
def convert_to_datetime(serie):
    return pd.to_datetime(serie)

##### MAIN #####

@exeTime
def main():
    
#### LA PARTIE GRISEE CI-DESSOUS CORRESPOND AU PREPROCESSING ENREGISTRE SOUS DF_NV.CSV ####

# --- CHOIX PARAMETRES ---

# #Le dataset chargé est déjà retravailler à partir de full_2020.csv comme suit:
# #Les colonnes retirées dans df_nv.csv sont :

# df_full_2020 = load_dataset('full_2020.csv')

# df0 = df_full_2020.drop(columns=['id_mutation',
#                   'numero_disposition',
#                   'adresse_numero',
#                   'adresse_suffixe',
#                   'adresse_code_voie',
#                   'code_commune',
#                   'ancien_code_commune',
#                   'ancien_nom_commune',
#                   'id_parcelle',
#                   'ancien_id_parcelle',
#                   'numero_volume',
#                   'lot1_numero',
#                   'lot1_surface_carrez',
#                   'lot2_numero',
#                   'lot2_surface_carrez',
#                   'lot3_numero',
#                   'lot3_surface_carrez',
#                   'lot4_numero',
#                   'lot4_surface_carrez',
#                   'lot5_numero',
#                   'lot5_surface_carrez',
#                   'code_nature_culture_speciale',
#                   'nature_culture_speciale',
#                   'code_nature_culture',
#                   'nature_culture',
#                     'code_postal',
#                     'code_type_local',
#                     'surface_terrain',
#                     'nombre_lots',
#                     'adresse_nom_voie',
#                   ])

# #uniformisation du type :
# df0['code_departement'] = df0['code_departement'].astype(str)

# # echantillon de 10% enregistré sous df_lite :
# #df_lite0 = df0.sample(frac=0.1, replace=True, random_state=1)



# # --- DONNEES A ETUDIER ---
# #df = load_dataset('df_lite.csv')

# #le dataset que je souhaite étudier dans un premier temps se focalise uniquement sur la valeur_fonciere manquante
# #df_nv.count() pour compter les valeurs manquantes facilement

# # renommer le type "Local industriel. commercial ou assimilé" en "Autre local"
# df0['type_local'] = df0['type_local'].replace({'Local industriel. commercial ou assimilé': 'Autre local'})

# #création d'un mask pour garder les valeurs nulles de valeur_fonciere
# df_nv_raw0 = use_mask(True, df0, 'valeur_fonciere')


# # je retire à présent la colonne des rpix
# df_nv = drop_col(df_nv_raw0, 'valeur_fonciere')

# #utiliser le format datetime de pandas
# df_nv['date'] = pd.to_datetime(df_nv['date_mutation'])

# #enregistrement dans un nouveau csv allégé pour l'étude à mener
# df_nv.to_csv('df_nv.csv', index=False)
    
#enregistrements des values_counts des types de locaux du dataset complet sous df0_type_vc.csv
# df0_type_vc = df0['type_local'].value_counts()
# df0_type_vc.to_csv('df0_type_vc.csv', index=False)    


    # --- STREAMLIT PAGE --- 
    

    df_nv = load_dataset('df_nv.csv')
    df0_type_vc = load_dataset('df0_type_vc.csv')
    #utiliser le format datetime de pandas
    df_nv['date'] = pd.to_datetime(df_nv['date_mutation'])
    
    #Introduction
    text = "Projet : Analyse du dataset 'Demande de valeurs foncières'"
    t = st.empty()
    for i in range(len(text) + 1):
        t.title("%s" % text[0:i])
        time.sleep(0.03)
    '____________'
    st.header(" Cette analyse se focalise sur les biens vendus dont la valeur foncière n'est pas renseignée." )
    st.write(" Quoi de plus étrange qu'un dataset de valeurs foncières avec des transactions sans montant indiqué ?")
    st.write(" Mon idée est simple : Chercher à savoir s'il s'agit de cas isolés ou bien s'il existe une tendance forte.")
    st.write(" Les critères étudiées seront : la localisation, le type de biens, les dates où l'on observe des transactions sans un prix renseigné.")
                                #st.write(" Pour l'exercice, je ne retiendrai qu'un echantillon de 10% des données initiales. Cet échantillon a été comparé aux résultats sur le dataset complet initial et ne déforme que très peu les résultats observés.")
                                #st.write("Ce dataset allégé contient 1,3% de montants transactionnelles non renseignées soit plus de 3100 sur cet échantillon d'environ 246 000 biens vendus.")
    '____________'
    
    
    # Date des prix manquants
    date_nv = get_feedback_nv(df_nv, 'date_mutation')
    date_nv.index.name = 'date'
    
    #Localisation des prix manquants
    departement_nv = get_feedback_nv(df_nv, 'code_departement')
    commune_nv = get_feedback_nv(df_nv, 'nom_commune')
    
    #Type des prix manquants
    type_nv = get_feedback_nv(df_nv, 'type_local')
    
    # Carte
    df_nv_longna = drop_na(df_nv, 'longitude') 
    df_nv_map = drop_na(df_nv_longna, 'longitude') #valeurs manquantes retirées
    
    # --- STREAMLIT ---
    
    st.subheader('Carte des montants transactionnels absents')
    
    if st.checkbox('Selectionner des filtres.', key='filtres'):
        
        # --- SIDEBAR --- # créations des différents champs pour filtrer la carte
        st.sidebar.title("Filtres de la carte")
    
        # filtre date avec choix sur calendrier    
        debut = datetime.date(2020,1,1)
        fin = datetime.date(2020,12,31)
        start_date = st.sidebar.date_input('Choisir une date de début', debut)
        end_date = st.sidebar.date_input('Choisir une date de fin', fin)
      
        if start_date > end_date or start_date < datetime.date(2020,1,1) or end_date > datetime.date(2020,12,31) :
            st.error('Erreur : Les dates spécifiées sont incohérentes')
        else:
            'Debut : ', start_date, ', Fin : ', end_date
        
        # filtre departement >> tapé par utilisateur
        option_dep = st.sidebar.text_input("choisir un code département",key=("dep"))
        if option_dep in df_nv['code_departement'].unique() :
            'Département : ', option_dep
        elif len(option_dep) <1 :
            pass
        else : st.error("Pas de résultats dans le département : `%s`" % option_dep)
        
        # filtre commune >> tapé par utilisateur
        option_com = st.sidebar.text_input("Choisir une commune",key=("com"))
        if option_com.capitalize() in df_nv['nom_commune'].unique() :
            'Commune : ', option_com.capitalize()
        elif len(option_com) <1 :
            pass        
        else : st.error("Pas de résultats dans la commune : `%s`" % option_com.capitalize())
    
        
        # filtre type >> selection multiple
        option_type = st.sidebar.multiselect("Choisir le type de bien",
                                            df_nv['type_local'].unique(),
                                            key="type")
        if len(option_type) > 0 :
            st.write('Types : ', *option_type)
    
        else :
            pass        
        # --- affichage avec filtre --- 
    
        # filtre nb de pièces avec condition sur type >> slider
        # Ce filtre n'est accessible que dans le cas d'une recherche d'appartement et/ou maison
        if any(e in ['Appartement','Maison'] for e in option_type):
            surface_min, surface_max = st.sidebar.slider('Choisir un nombre de pièces principales (logement)',
                                                      int(df_nv['nombre_pieces_principales'].min()),
                                                      int(df_nv['nombre_pieces_principales'].max()),
                                                      (int(df_nv['nombre_pieces_principales'].min()),
                                                      int(df_nv['nombre_pieces_principales'].max())),
                                                      1,
                                                      key='rooms')
    
        # --- AFFICHAGE DES FILTRES --- 
    
        #date
        if True:
            df_nv_map = use_mask_sup(pd.to_datetime(start_date),df_nv_map,'date')
            df_nv_map = use_mask_inf(pd.to_datetime(end_date),df_nv_map,'date')
            
        #departement
        if len(option_dep) > 0 :
            df_nv_map = use_mask(option_dep, df_nv_map, 'code_departement')
        
        #commune
        if len(option_com) > 0 :
            df_nv_map = use_mask(option_com.capitalize(), df_nv_map, 'nom_commune')
    
        #type
        if len(option_type) > 0 :
            df_nv_map = use_mask_isin(option_type, df_nv_map, 'type_local')
            
        #pieces
        if any(e in ['Appartement','Maison'] for e in option_type):
            df_nv_map = use_mask_inf(surface_max, df_nv_map,'nombre_pieces_principales')
            df_nv_map = use_mask_sup(surface_min, df_nv_map,'nombre_pieces_principales')
    st.map(df_nv_map)
    st.subheader("Liste détaillée des transactions affichées sur la carte")
    st.dataframe(df_nv_map)

    '____________'
    
    st.write("N.B. Les pourcentages correspondent à la proportion sur le dataset complet sauf indication contraire")
    
    # Histogramme de dates
    st.subheader('Top 5 des dates de transactions sans prix renseigné')
    st.bar_chart(date_nv['pourcentage'].head(5))
    
    
    st.write("<font color='orange'>On observe une grande majorité de cas le 09 novembre</font>", unsafe_allow_html=True)
    st.write("<font color='lightgreen'>Valeurs manquantes dans la colonne 'date' : </font>",
              100*round(1-len(drop_na(df_nv,'date'))/len(df_nv.index),1),
              "<font color='lightgreen'>%</font>", unsafe_allow_html=True)
    
    '____________'
    # histo type de biens
    st.subheader('Types de biens sans montant renseigné')
    sel_type = st.selectbox('Afficher tout confondu ou par type ?',
                            ['tous types confondus (valeurs manquantes incluses)','par type (valeurs manquantes excluses)'],
                            key='type')
    
    if sel_type == 'tous types confondus (valeurs manquantes incluses)':
        
        sns.set_theme(style="whitegrid")
        fig2,ax2 = plt.subplots()
        ax2 = sns.barplot(x=type_nv.index, y=type_nv['pourcentage'], data = type_nv)
        st.pyplot(fig2)
    else : 
        # camembert des types de bien
        type2 = round((df_nv['type_local'].value_counts()/df0_type_vc),3)*100
        fig1,ax1 = plt.subplots()
        ax1.pie(type2, labels=type_nv.index, autopct='%1.1f%%')
        ax1.axis('equal')
        st.pyplot(fig1)
        
    st.write("<font color='orange'>On observe une plus grande tendance de 'Appartement' et 'Dépendence' alors que 'Maison' est le plus répandu sur le dataset complet</font>", unsafe_allow_html=True)
    st.write("<font color='red'>Valeurs manquantes dans la colonne 'type_local' : </font>",
              100*round(1-len(drop_na(df_nv,'type_local'))/len(df_nv.index),1),
              "<font color='red'>%</font>", unsafe_allow_html=True)
    '____________'
    # Localisation
    st.subheader('Top 5 des départements avec transactions sans prix renseigné')
    st.bar_chart(departement_nv['pourcentage'].head(5))
    
    st.write("<font color='orange'>On observe une concentration accrue dans le département de l'Oise(60) </font>", unsafe_allow_html=True)
    st.write("<font color='lightgreen'>Valeurs manquantes dans la colonne 'code_departement' : </font>",
              100*round(1-len(drop_na(df_nv,'code_departement'))/len(df_nv.index),1),
              "<font color='lightgreen'>%</font>", unsafe_allow_html=True)
    '____________'
    st.subheader('Top 5 des communes avec transactions sans prix renseigné')
    st.bar_chart(commune_nv['pourcentage'].head(5))
    
    st.write("<font color='orange'>Sans surprise, une grande ville de l'Oise ressort : Compiègne </font>", unsafe_allow_html=True)
    st.write("<font color='lightgreen'>Valeurs manquantes dans la colonne 'nom_commune' : </font>",
              100*round(1-len(drop_na(df_nv,'nom_commune'))/len(df_nv.index),1),
              "<font color='lightgreen'>%</font>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    st.write("")
    '____________'
    st.write("C'est ici que s'achève cette brève étude.")
    st.write("N'oubliez pas d'aller voir le formulaire permettant de filtrer la carte selon vos critères !")

### lancement du main ###

if __name__ == "__main__":
    main()