import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
bmi = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (bmi > 25).astype(int)

#3
normalize = ['cholesterol', 'gluc']
for col in normalize:
    df.loc[df[col] == 1, col] = 0
    df.loc[df[col] > 1, col] = 1

# 4
def draw_cat_plot():
    # 5
    df_cat = df.melt(id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    

    # 7
    fig = sns.catplot(data=df_cat,
                      x='variable',
                      y='total',
                      hue='value',
                      col='cardio',
                      kind='bar',
                      height=6,
                      aspect=1).fig 

    # 8
    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    pressure = (df['ap_lo'] <= df['ap_hi'])
    height = ((df['height'] >= df['height'].quantile(0.025)) 
              & (df['height'] <= df['height'].quantile(0.975)))
    weight = ((df['weight'] >= df['weight'].quantile(0.025)) 
              & (df['weight'] <= df['weight'].quantile(0.975)))

    filtered_data = pressure & height & weight

    df_heat = df[filtered_data]

    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14
    fig, ax = plt.subplots(figsize=(12,10))

    # 15
    sns.heatmap(
        corr,
        mask=mask,          # Apply the mask to hide the upper triangle
        annot=True,         # Show the correlation values on the heatmap
        fmt='.1f',          # Format annotations to one decimal place
        linewidths=.5,      # Add lines between cells
        cmap='coolwarm',    # Use a diverging colormap
        center=0,           # Center the colormap at 0
        ax=ax               # Draw the heatmap on the pre-defined axes
    )


    # 16
    fig.savefig('heatmap.png')
    return fig
