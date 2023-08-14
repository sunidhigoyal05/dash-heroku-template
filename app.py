import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

df = gss_clean.groupby('sex').agg({'income':'mean','job_prestige':'mean','socioeconomic_index':'mean','education':'mean'}).reset_index()
df = df.rename({'income':'Mean_Income','job_prestige':'Mean_Job_Prestige_Score','socioeconomic_index':'Mean_socioeconomic_index','education':'Mean_Years_Of_Education'},axis=1)
df = round(df,2)
table = ff.create_table(df)
table.show()       
          
sex_breadwinner = gss_clean.groupby('sex').agg({'male_breadwinner':'count'}).reset_index()
fig1 = px.bar(sex_breadwinner, x='sex', y='male_breadwinner',color = 'sex',height = 400, width = 500,color_discrete_map = {'male':'blue', 'female':'magenta'},
            labels = {'sex': 'Sex of the Respondent', 'male_breadwinner': 'Number of People who want a male breadwinner'},
            )
fig1.update_layout(showlegend=False)
fig1.update(layout=dict(title=dict(x=0.5)))
fig1.show()

fig2 = px.scatter(gss_clean,
                 x = 'job_prestige',
                 y = 'income',
                height = 600, width = 600, 
                color = 'sex',
                color_discrete_map = {'male':'blue', 'female':'magenta'},
                trendline = 'ols',
                labels = {'job_prestige': 'Occupational Prestige Score of the Respondent', 'income': 'Income of the Respondent'},
                hover_data = ['education','socioeconomic_index']
                )
fig2.update_layout(showlegend=True)
fig2.update(layout=dict(title=dict(x=0.5)))
fig2.show()

fig3 = px.box(gss_clean,
             y = 'income',
             x = 'sex',
             color = 'sex',
             height = 600,
             width = 600,
             color_discrete_map = {'male':'blue', 'female':'magenta'},
             labels = {'income': 'Income of the Respondent', 'sex': 'Sex of the Respondent'},
            )
fig3.update(layout=dict(title=dict(x=0.5)))
fig3.update_layout(showlegend=False)
fig3.show()

fig4 = px.box(gss_clean,
             y = 'job_prestige',
             x = 'sex',
             color = 'sex',
             height = 600,
             width = 600,
             color_discrete_map = {'male':'blue', 'female':'magenta'},
             labels = {'job_prestige': 'Occupational Prestige Score of the Respondent', 'sex': 'Sex of the Respondent'},
            )
fig4.update(layout=dict(title=dict(x=0.5)))
fig4.update_layout(showlegend=False)
fig4.show()


new_gss = gss_clean[['income','sex','job_prestige']]
new_gss['occupational_prestige_score_range'] = pd.cut(new_gss['job_prestige'], bins = 6)
new_gss = new_gss.dropna()

fig5 = px.box(new_gss,
             x = 'sex',
             y = 'income',
             height = 2000, width = 1200,
             color = 'sex',
             color_discrete_map = {'male':'blue', 'female':'magenta'},
             facet_col = 'occupational_prestige_score_range', 
             facet_col_wrap = 2,
             labels = {'income': 'Income of the Respondent', 'sex': 'Sex of the Respondent'},
            )
fig5.update(layout=dict(title=dict(x=0.5)))
fig5.update_layout(showlegend=False)
fig5.show()

import dash_bootstrap_components as dbc
image_path = 'https://github.com/sunidhigoyal05/dash-heroku-template/tree/6f37d7256a31ce35f952b705ed32b69fc308679f/assets/image.png'

external_stylesheets = [dbc.themes.QUARTZ]
app = JupyterDash(__name__, external_stylesheets = external_stylesheets)

mymarkdowntext = '''


*_The Gender Wage Gap_* \n

The disparity in earnings between men and women is referred to as the gender wage gap.Women regularly earn less than males, and the disparity is bigger for most women of colour. Experts have computed this gap in a multitude of ways, but despite the many estimates, there is agreement on this issue.
According to an analysis of the most current Census Bureau statistics from 2018, women of all races made just 82 cents for every dollar that males of all races made.The cumulative negative impacts of numerous prejudices on earnings are also felt by those who live intersectional realities, such as transgender women and immigrant women.
To determine the particular locations of wage gaps and the areas in which they must be addressed, much more data—disaggregated by sex, race and ethnicity, gender identity, sexual orientation, handicap status, and other factors—is necessary.


*_The General Society Survey_*\n

The General Society Survey, abbreviated as GSS, gathers information about modern American society to track and analyse societal developments in opinions, attitudes, and behaviours, The GSS has modified past polls' questions, enabling comparisons. It includes subjects of particular relevance in addition to the typical core of questions on demographic, behavioural, and attitudinal characteristics. Civil freedoms, crime and violence, intergroup tolerance, morality, national spending priorities, psychological well-being, social mobility, stress and traumatic experiences are some of the subjects explored. It enables researchers to explore the functioning and framework of the society, and it also gives them context to compare the US with other nations. 

Sources: \n 

http://www.gss.norc.org/About-The-GSS

https://www.americanprogress.org/article/quick-facts-gender-wage-gap/



'''


app.layout = html.Div([
    
    
    html.H1("A Study of Interaction between Income and Gender"),
    
    
    
   
    
    dcc.Markdown(children = mymarkdowntext),
    
    

    html.H2("Average of Contributing Factors"),
        
    dcc.Graph(figure=table),
    
    html.H2("Barplot - Agreement to Statements vs Sex, Region or Education"),
    
    dcc.Dropdown(id = 'y-axis',
                 options = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']
                 ),
    
    dcc.Dropdown(id = 'grouper',
                 options = ['sex','region','education' ]
                 ),
        

    
    
    
        
    dcc.Graph(id = 'barplot'),
    

        
        
        
        
        
        
    html.H2("Occupational Prestige Score vs Income of the Respondent"),
        
        dcc.Graph(figure=fig2),
        
    
        
    
    
        
    html.Div([
            
            html.H2("Income of the Respondent Vs Sex of the Respondent"),
            
            dcc.Graph(figure=fig3)
            
        ], style = {'width':'47%', 'float':'left'}),
        
    html.Div([
            
            html.H2("Occupational Prestige Score Vs Sex of the Respondent"),
            
            dcc.Graph(figure=fig4)
            
        ], style = {'width':'47%', 'float':'right'}),
    
    
    html.H2("Study of Income of the Respondent vs Sex, with Occuptional Prestige Score Range in Perspective"),
        
        dcc.Graph(figure=fig5)
        
    
])

if __name__ == '__main__':
    app.run_server(debug = True, port = 8025)

@app.callback(Output(component_id = 'barplot',component_property = 'figure'),
              
              [
               Input(component_id = 'grouper', component_property = 'value'),
               Input(component_id = 'y-axis',component_property = 'value')
               ])

def malebreadwinner(grouper,bars_for):
    sex_breadwinner = gss_clean.groupby(by = grouper, level = None).agg({bars_for:'count'}).reset_index()
    barplot = px.bar(sex_breadwinner, x=grouper, y=bars_for,color = grouper
            )
    barplot.update_layout(showlegend=False)
    barplot.update(layout=dict(title=dict(x=0.5)))
    return barplot 

