from tabulate import tabulate
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as mp

shooting = pd.read_csv("Data/shooting.csv")
goal_points = pd.read_csv("Data/goal_points.csv")
defense = pd.read_csv("Data/defense.csv")
shooting.head(5)
zones = {
    'restricted': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM', 'FGA', 'FG_PCT'],
    'paint': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM.1', 'FGA.1', 'FG_PCT.1'],
    'mid_range': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM.2', 'FGA.2', 'FG_PCT.2'],
    'left_corner': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM.3', 'FGA.3', 'FG_PCT.3'],
    'right_corner': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM.4', 'FGA.4', 'FG_PCT.4'],
    'corner': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM.7', 'FGA.7', 'FG_PCT.7'],
    'above_the_break': ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM.5', 'FGA.5', 'FG_PCT.5']
}


def print_data(data):
    pdtabulate = lambda data: tabulate(data, headers='keys', tablefmt='psql')
    print(pdtabulate(data))


column_names = ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'FGM', 'FGA', 'FG_PCT', 'PLAYER_POSITION', 'FG2M',
                'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT']

# By the following block code we join players' three datasets 'shooting', 'goal_points' and 'defense' to have seven
# datasets for each zone (part of court) with their specific values such as field goals made, field goals attempted and
# field goal percentage. Besides that, we also include 2 and 3 point field goals made, attempted and percentage, and
# also positions which is the most important factor in the dataset that we will get.
for area in zones:
    data_frame = pd.DataFrame()
    for column in zones[area]:
        data_frame[column] = shooting[column]
    data = data_frame.merge(defense[['PLAYER_NAME', 'PLAYER_POSITION']]).merge(
        goal_points[['PLAYER_NAME', 'FG2M', 'FG2A', 'FG2_PCT',
                     'FG3M', 'FG3A', 'FG3_PCT']])
    data.columns = column_names
    data.to_csv("Data/" + area + "_area.csv", index=False)

# # As the zone datasets contain "nan" values we replace them with the mean of the corresponding column. We also need
# # to round columns and fix the columns of percentage.
zones_names = ['restricted', 'paint', 'mid_range', 'left_corner', 'right_corner', 'corner', 'above_the_break']
for zone in zones_names:
    data = pd.read_csv("Data/" + zone + "_area.csv")
    data[column_names] = data[column_names].fillna(value=data[column_names].mean(numeric_only=True))
    data[['FG2M', 'FG2A', 'FG3M', 'FG3A']] = data[['FG2M', 'FG2A', 'FG3M', 'FG3A']].round(decimals=1)
    data[['FG_PCT', 'FG2_PCT', 'FG3_PCT']] = data[['FG_PCT', 'FG2_PCT', 'FG3_PCT']].apply(lambda x: x * 100)
    data.to_csv("Data/" + zone + "_area.csv", index=False)


# # The next step is grouping each zone dataset by players' positions by using mean function to calculate the average
# # data of each position. In order to have an accurate data after the grouping we again round the values.
def group_zones(zone, zone_data):
    grouped_data = zone_data.groupby('PLAYER_POSITION').mean()
    grouped_data[['FGM', 'FGA', 'FG_PCT', 'FG2M', 'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT']] = \
        grouped_data[['FGM', 'FGA', 'FG_PCT', 'FG2M', 'FG2A', 'FG2_PCT', 'FG3M', 'FG3A', 'FG3_PCT']].round(decimals=1)
    grouped_data.to_csv("Data/"  + zone + "_area.csv")


for zone in zones_names:
    data = pd.read_csv("Data/" + zone + "_area.csv")
    cleaned = data.drop(['TEAM_ABBREVIATION', 'PLAYER_NAME', 'AGE'], axis=1)
    group_zones(zone, cleaned)

# Calculating Effective Field Goal Percentage Calculator (2pt FGM + 1.5 * 3pt FGM) / FGA
for zone in zones_names:
    data = pd.read_csv("Data/" + zone + "_area.csv")
    data['Effective_Field_Goal_PCT'] = (data['FG2M'] + (1.5 * data['FG3M'])) / data['FGA']
    data['Effective_Field_Goal_PCT'] = data['Effective_Field_Goal_PCT'].round(decimals=1)
    data.to_csv("Data/"  + zone + "_area.csv", index=False)


def plot_barplots():
    for zone in zones_names:
        data = pd.read_csv("Data/"  + zone + "_area.csv")
        sns.barplot(data=data, x="PLAYER_POSITION", y="Effective_Field_Goal_PCT") \
            .set(xlabel='PLAYER POSITION', ylabel='Effective Field Goal Percentage (eFG%)',
                 title=f'Effective Field Goal Percentage (eFG%) of player positions in the {zone.replace("_", " ")} zone')
        plt.show()


plot_barplots()

merged_zones = []
for zone in zones_names:
    data = pd.read_csv("Data/"  + zone + "_area.csv")
    data['ZONE'] = zone
    merged_zones.append(data)
merged_zones = pd.concat(merged_zones)
merged_zones.reset_index(drop=True, inplace=True)

print_data(merged_zones)
merged_zones = merged_zones.groupby('PLAYER_POSITION').mean()
print_data(merged_zones)

sns.relplot(x='FG2M', y='FG3M', data=merged_zones, kind='scatter', s=100, style='PLAYER_POSITION', hue='PLAYER_POSITION');
mp.show()