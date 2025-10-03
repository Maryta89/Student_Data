import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import os

# -------------------
# Load and clean data
# -------------------
file_path = "student_data.csv"
df = pd.read_csv(file_path)

# Drop duplicates
df = df.drop_duplicates()

# Handle missing values safely
for col in df.columns:
    if df[col].dtype in ['int64', 'float64']:
        df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] = df[col].fillna(df[col].mode()[0])

# -------------------
# Create visualizations with real columns
# -------------------
# 1. Distribution of Age
fig1 = px.histogram(df, x="age", title="Distribution of Age")

# 2. Boxplot of Final Grade (G3)
fig2 = px.box(df, y="G3", title="Boxplot of Final Grade (G3)")

# 3. Scatter Plot: Study Time vs Final Grade, colored by Sex
fig3 = px.scatter(df, x="studytime", y="G3", color="sex", title="Study Time vs Final Grade by Sex")

# 4. Bar Chart: Average Final Grade by School
fig4 = px.bar(df.groupby("school", as_index=False)["G3"].mean(), x="school", y="G3", title="Average Final Grade by School")

# 5. Pie Chart: Distribution of Students by Address (Urban vs Rural)
fig5 = px.pie(df, names="address", title="Distribution by Address")

# 6. Line Chart: Absences vs Final Grade
fig6 = px.line(df, x="absences", y="G3", title="Absences vs Final Grade")

# -------------------
# Save figures as images in current folder
# -------------------
output_dir = os.path.dirname(os.path.abspath(__file__))

fig1.write_image(os.path.join(output_dir, "fig1_distribution_age.png"))
fig2.write_image(os.path.join(output_dir, "fig2_boxplot_g3.png"))
fig3.write_image(os.path.join(output_dir, "fig3_scatter_studytime_g3.png"))
fig4.write_image(os.path.join(output_dir, "fig4_bar_school_g3.png"))
fig5.write_image(os.path.join(output_dir, "fig5_pie_address.png"))
fig6.write_image(os.path.join(output_dir, "fig6_line_absences_g3.png"))

# -------------------
# Build dashboard
# -------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Student Data Dashboard"),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6)
])

if __name__ == "__main__":
    app.run(debug=True)