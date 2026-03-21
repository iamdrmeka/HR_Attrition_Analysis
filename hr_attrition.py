import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Import Dataframe
df = pd.read_csv('hr_project.csv')
df.sample(2)
# Remove spaces and turn everything to lower case for ease of access.
for cols in df.select_dtypes(include=["object", 'string']):
    df[cols] = df[cols].astype(str).str.strip().str.lower()
# add _ to the column names for better readability, then make lower case for ease of selection
df.columns = df.columns.str.replace(
    r'(?<!^)(?=[A-Z])', '_', regex=True).str.lower()
# drop duplicates
df = df.drop_duplicates()

# olot title style
title_font = {
    'fontname': 'Arial',
    'fontweight': 'bold',
    'fontsize': 14
}
# label funciton


def chat_labels(xlabels, ylabels, size=12, weight='bold'):
    plt.xlabel(xlabels, fontsize=size, fontweight=weight)
    plt.ylabel(ylabels, fontsize=size, fontweight=weight)


bar_color = '#0508B3'


# Group salaries
df['salary_range'] = pd.cut(
    df['monthly_income'],
    bins=[1, 5000, 9000, 12500, 16000, 30000],
    labels=['below 5,000',
            '5,001 - 9,000',
            '9,001 - 12,500',
            '12,501 - 16,000',
            '16,001 and above'
            ]
)

# get customer churn information
attrited = df[df['attrition'] == 'yes']['employee_number'].nunique()
active_employee = all_staff - attrited
attrition_rate = round((100 * attrited) / all_staff, 2)

# 3Organise the data in a data frame
attrition_table = pd.DataFrame({
    'Details': ['Total Staff', 'Active Employees', 'Attrited', 'Attrition Rate'],
    'Values': [all_staff, active_employee, attrited, attrition_rate]
})
display(attrition_table)

# Pie chat for attrition rate

plt.figure(figsize=(4, 4))  # create figure and size

# Plot the pie chat
w, labels, percnts = plt.pie(attrition_table.loc[1:2, 'Values'],
                             colors=['#0508B3', "#D80C49"],
                             explode=[0, 0.1],
                             labels=attrition_table.loc[1:2, 'Details'],
                             startangle=45,
                             autopct='%.2f%%')

# Add font weight tot he labels
for lbl in labels:
    lbl.set_fontweight('bold')

# add colors and font weight to the % values
for cents in percnts:
    cents.set_color('white')
    cents.set_fontweight('bold')

plt.title(f"Employee Attrtion Rate: {attrition_rate:,.2f}%",
          **title_font)
plt.show()

# Department Exploration

# Get total department staff
depts = df.groupby('department')['employee_number'].nunique()

# Get number of atttrition
dept_attrition = (df[df['attrition'] == 'yes']
                  .groupby('department')
                  ['employee_number'].nunique())

# combine tables debt and dept attrition
dept_table = pd.concat([depts, dept_attrition], axis=1)

# Rename columns
dept_table.columns = ['Total Staff', 'Attrited']

# calculate churn rate
dept_table['Attrition Rate'] = round((100 * dept_attrition) / depts, 2)

# Reset Index
dept_table.reset_index(inplace=True)

# Clean string and columns
dept_table['department'] = dept_table['department'].str.title()
dept_table.columns = dept_table.columns.str.title()
dept_table


# Sort by total staff
dept_table = dept_table.sort_values(by='Total Staff', ascending=False)

plt.figure(figsize=(8, 6))

bars = plt.bar(
    dept_table['Department'],
    dept_table['Total Staff'],
    color='#0508B3'
)

# Title and labels
plt.title(
    "Department Staff Distribution",
    fontsize=16,
    fontweight='bold',
    pad=15
)

plt.ylabel('Staff Count', fontsize=12)
plt.xlabel('Department', fontsize=12)

# Clean x-axis labels (capitalize)
plt.xticks(

    rotation=20
)

# Add subtle gridlines
plt.grid(axis='y', linestyle='dashed', alpha=0.3)


# Add data labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f'{int(height)}',
        ha='center',
        va='bottom',
        fontsize=10
    )


ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Adjust layout
plt.tight_layout()

plt.show()


# Sort by Attrition rate
dept_table = dept_table.sort_values(by='Attrition Rate', ascending=False)

plt.figure(figsize=(8, 6))

bars = plt.bar(
    dept_table['Department'],
    dept_table['Attrition Rate'],
    color='#0508B3'
)

# Title and labels
plt.title(
    "Attrition Rate by Departments",
    fontsize=16,
    fontweight='bold',
    pad=15
)

plt.ylabel('Attrition Rate', **title_font)

plt.xlabel('Departments', **title_font)


plt.xticks(rotation=20
           )

# Add subtle gridlines
plt.grid(axis='y', linestyle='dashed', alpha=0.3)


# Add data labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f'{int(height)}%',
        ha='center',
        va='bottom',
        fontsize=10
    )

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Adjust layout
plt.tight_layout()

plt.show()


# calculate number of staff who scored what in job satisfaction survey
score_one = (df[(df['job_satisfaction'] == 1)
                & (df['attrition'] == 'yes')]
             .groupby('department')['employee_number']).nunique()

score_two = (df[(df['job_satisfaction'] == 2)
                & (df['attrition'] == 'yes')]
             .groupby('department')['employee_number']).nunique()

score_three = (df[(df['job_satisfaction'] == 3)
                  & (df['attrition'] == 'yes')]
               .groupby('department')['employee_number']).nunique()

score_four = (df[(df['job_satisfaction'] == 4)
                 & (df['attrition'] == 'yes')]
              .groupby('department')['employee_number']).nunique()

# GEt percentages score_one_pecnt  = round((100 * score_one) / dept_attrition, 2)
score_one_pecnt = round((100 * score_one) / dept_attrition, 2)
score_two_pecnt = round((100 * score_two) / dept_attrition, 2)
score_three_pecnt = round((100 * score_three) / dept_attrition, 2)
score_four_pecnt = round((100 * score_four) / dept_attrition, 2)

# Merge table and remane columnsd
satisfaction_table = (pd.concat([dept_attrition,
                                 score_one_pecnt,
                                 score_two_pecnt,
                                 score_three_pecnt,
                                 score_four_pecnt], axis=1))
satisfaction_table.columns = ['Attrited', 'Poor', 'Fair', 'Good', 'Very Good']
satisfaction_table.reset_index(inplace=True)

# clean columns
satisfaction_table.columns = satisfaction_table.columns.str.title()
satisfaction_table['Department'] = satisfaction_table['Department'].str.title()
display(satisfaction_table)


# Plot Satisfaction Scores Across Departments
satisfaction_table.set_index('Department')[['Poor', 'Fair', 'Good', 'Very Good']].plot(
    kind='bar',
    figsize=(10, 6),
    color=['red', 'orange', 'lightgreen', 'forestgreen']
)

plt.title(' Job Satisfaction Scores Across Departments',
          fontsize=20,
          fontweight='bold',
          pad=20,
          fontname='Arial'
          )
plt.grid(axis='y', linestyle='solid', alpha=0.5)
plt.ylabel('Percentage (%)')
plt.xlabel('Departments', fontweight='bold', labelpad=20)
plt.xticks(rotation=1)
plt.tight_layout()
lines = plt.gca()
lines.spines['top'].set_visible(False)
lines.spines['right'].set_visible(False)
plt.show()

# Gender and attrition
gender_count = df.groupby('gender')['employee_number'].nunique()
gender_attrited = df[df['attrition'] == 'yes'].groupby(
    'gender')['employee_number'].nunique()
gender_table = pd.concat([gender_count, gender_attrited], axis=1)
gender_table.columns = ['Staff', 'Attrited']
gender_table['Attrition Rate'] = round((100 * gender_attrited)/gender_count, 2)
gender_table = gender_table.reset_index()

# gender_table.reset_index(inplace=True)
gender_table.columns = gender_table.columns.str.title()
gender_table['Gender'] = gender_table['Gender'].str.title()

w, t, percents = plt.pie(gender_table['Staff'],
                         explode=[0.05, 0],
                         autopct='%.2f%%',
                         labels=gender_table['Gender'],
                         colors=["#D80C49", "#0508B3"],
                         startangle=270
                         )

for cents in percents:
    cents.set_color('white')
    cents.set_fontweight('bold')

plt.title("Gender Distribution", fontname='arial', fontweight='bold')
plt.show()
# plot for gender attrtion rate
gender_table = gender_table.sort_values(by="Attrition Rate", ascending=False)
plt.bar(gender_table['Gender'],
        gender_table['Attrition Rate'], color='#0508B3')
plt.title('Attrition Rate By Gender')
plt.xlabel('Genders', fontweight='bold', fontname="Arial")
plt.ylabel('Attrtion rate (%)')
plt.grid(axis='y', linestyle='dashed', alpha=0.1)
lines = plt.gca()
lines.spines['top'].set_visible(False)
lines.spines['left'].set_visible(False)
lines.spines['right'].set_visible(False)

# create an age group column
df['age_group'] = pd.cut(
    df['age'],
    bins=[1, 26, 35, 44, 52, 60],
    labels=[
        '18-26',
        '27-35',
        '36-44',
        '45-52',
        '53-60'

    ]
)

# AGE GROUP SCRIPT
age_groups_vol = df.groupby('age_group')['employee_number'].nunique()

age_group_att = df[df['attrition'] == 'yes'].groupby(
    'age_group')['employee_number'].nunique()

age_group_table = pd.concat([age_groups_vol, age_groups_vol], axis=1)

age_group_table.columns = ['Staff Count', 'Attrition']

age_group_table['Attrition Rate'] = round(
    (100 * age_group_att) / age_groups_vol, 2)

age_group_table = age_group_table.reset_index()

age_group_table.columns = age_group_table.columns.str.title()
age_group_table

# Plot for age groups staff Distr
age_group_table.sort_values(by='Staff Count', ascending=False, inplace=True)
plt.bar(age_group_table['Age_Group'],
        age_group_table['Staff Count'], color=bar_color)
plt.title('Staff Distribution by Age Groups', **title_font)
chat_labels('Age Groups', 'Staff Count', size=12, weight='bold')
lines = plt.gca()
lines.spines['top'].set_visible(False)
lines.spines['right'].set_visible(False)
plt.grid(axis='y', linestyle='solid', alpha=0.3)
plt.show()

# Plot for age groups and atrition

age_group_table.sort_values(by='Attrition Rate', ascending=False, inplace=True)
plt.bar(age_group_table['Age_Group'],
        age_group_table['Attrition Rate'], color=bar_color)
plt.title('Attrition Rate by Age Groups', **title_font)
chat_labels('Age Groups', 'Attrition Rate', size=12, weight='bold')
lines = plt.gca()
lines.spines['top'].set_visible(False)
lines.spines['right'].set_visible(False)
plt.grid(axis='y', linestyle='solid', alpha=0.3)
plt.show()

job_satisfaction = df.groupby('age_group')['job_satisfaction'].mean()
job_satisfaction = job_satisfaction.reset_index()
job_satisfaction['job_satisfaction'] = job_satisfaction['job_satisfaction'].apply(
    lambda x: round(x, 2))
job_satisfaction
# Average Job satisfaction Remain the same overall

# marital status
ms = df.groupby('marital_status')['employee_number'].nunique()
ms_a = df[df['attrition'] == 'yes'].groupby(
    'marital_status')['employee_number'].nunique()
a_a = round((100 * ms_a) / ms, 2)
Marital_status_table = pd.concat([ms, ms_a, a_a], axis=1)

Marital_status_table.columns = [
    'Total Staff', 'Attried Staff', 'Attrition Rate']
Marital_status_table = Marital_status_table.reset_index()
Marital_status_table = pd.concat([ms, ms_a, a_a], axis=1)

Marital_status_table.columns = [
    'Total Staff', 'Attried Staff', 'Attrition Rate']
Marital_status_table = Marital_status_table.reset_index()

# Plot for marital status staff count and attrition rate

# Staff Count
Marital_status_table = Marital_status_table.sort_values(
    by='Total Staff', ascending=False)
Marital_status_table.set_index('marital_status')['Total Staff'].plot(
    kind='bar',
    figsize=(8, 6),
    color=bar_color
)
chat_labels('Marital Status', 'Staff Count', size=12, weight='bold')
plt.title('Staff Distribution by Marital Status',
          fontname="Arial", fontweight='bold', pad=5)
plt.grid(axis='y', linestyle='dashed', alpha=0.5)
plt.show()

# Attrition_rate
Marital_status_table = Marital_status_table.sort_values(
    by='Attrition Rate', ascending=False)
Marital_status_table.set_index('marital_status')['Attrition Rate'].plot(
    kind='bar',
    figsize=(8, 6),
    color=bar_color
)
chat_labels('Marital Status', 'Attrition Rate', size=12, weight='bold')
plt.title('Attrition by Marital Status',
          fontname="Arial", fontweight='bold', pad=5)
plt.grid(axis='y', linestyle='dashed', alpha=0.5)
plt.tight_layout()
plt.show()

# educational field
edu_feilds = df.groupby('education_field')['employee_number'].nunique()
edu_feilds_att = df[df['attrition'] == 'yes'].groupby(
    'education_field')['employee_number'].nunique()
edu_table = pd.concat([edu_feilds, edu_feilds_att], axis=1)
edu_table.columns = ['Total Staff', 'Attrited Staff']
edu_table['Attrition Rate'] = round((100 * edu_feilds_att) / edu_feilds, 2)
edu_table.columns = edu_table.columns.str.title()
edu_table.columns = edu_table.columns.str.title()
edu_table.reset_index(inplace=True)
edu_table['education_field'] = edu_table['education_field'].str.title()
display(edu_table)


# plot for educational status and attrition rate
fig, ax1 = plt.subplots(figsize=(8, 5))

colors = ['#0508B3', '#d18080']

ax1.bar(edu_table['education_field'],  edu_table['Total Staff'], label='Total Staff',
        color=colors[0]
        )

ax1.bar(
    edu_table['education_field'], edu_table['Attrited Staff'],
    label='Attrited Staff', color=colors[1]
)

ax1.set_xlabel('Education Field', labelpad=20, fontweight='bold')
ax1.set_ylabel('Staff Count')

ax2 = ax1.twinx()
ax2.plot(edu_table['education_field'],
         edu_table['Attrition Rate'],   marker='o', linestyle='--',  color='#D80C49'
         )

ax2.set_ylabel('Attrition Rate (%)')

plt.title('Staff Count & Attrition Rate by Education Field')
fig.legend(loc='upper right')
# rotate the edu fields
for label in ax1.get_xticklabels():
    label.set_rotation(30)
plt.tight_layout()
plt.show()

# Create a function for the attrtion tables calculation to avoid repititive codes


def attrition_tables(grouper, df=df, identity='employee_number',
                     filter_col='attrition', filter_val='yes'):

    total_staff = df.groupby(grouper)[identity].nunique()

    attrited = (df[df[filter_col] == filter_val].
                groupby(grouper)[identity].nunique()
                )

    att_table = pd.concat([total_staff, attrited], axis=1)

    att_table.columns = ['Total Staff', 'Attrited Staff']

    att_table['Attrition Rate'] = (((100 * att_table['Attrited Staff'])
                                    / att_table['Total Staff']).round(2))
    att_table = att_table.reset_index()
    # clean
    att_table.columns = att_table.columns.str.title()

    return att_table


# JOb role analysis
job_role = attrition_tables('job_role')
job_role
# job_role[Job_Role] = job_role[Job_Role].str.title()

job_role.sort_values(by='Total Staff', ascending=False, inplace=True)
fig, mybar = plt.subplots(figsize=(8, 6))

mybar.bar(job_role['Job_Role'], job_role['Total Staff'],
          color='#050883', label='Total Staff')
myline = mybar.twinx()
myline.plot(job_role['Job_Role'], job_role['Attrition Rate'],
            color='red', linestyle='dashed', marker='o')
mybar.set_xlabel("Job Role", fontweight='bold')
mybar.set_ylabel('Staff Count')
myline.set_ylabel("Attrition Rate")
fig.legend(loc='upper right')
plt.title('Jobe role and Atrition Rate', **title_font)
for roles in mybar.get_xticklabels():
    roles.set_rotation(72)
plt.grid(axis='y', linestyle='solid', alpha=0.5)
plt.show()

# Job role analysis
job_level = attrition_tables('job_level')
job_level

# plot for  Job level

fig, mybar = plt.subplots(figsize=(8, 6))
mybar.bar(job_level['Job_Level'], job_level['Total Staff'],
          color='#050883', label='Total Staff')
myline = mybar.twinx()

myline.plot(job_level['Job_Level'],  job_level['Attrition Rate'],
            marker='v', color="#C20404", label='Attrited')
myline.set_ylabel('Attrition Rate (%)', fontname='Arial')
mybar.set_ylabel('Staff Count', fontname='Arial')
mybar.set_xlabel('Job Levels', fontweight='bold', fontname='Arial')
plt.grid(axis='y', linestyle='dashed', alpha=0.5)
fig.legend(loc='upper right')
plt.title('Job Level and Attrition', **title_font)
plt.tight_layout()
plt.show()

# job involvement
job_involvement = attrition_tables('job_involvement')
job_involvement = job_involvement.sort_values(
    by='Total Staff', ascending=False)

job_involvement
# plot for job involvement
fig, mybar = plt.subplots(figsize=(8, 6))
x_labels = job_involvement['Job_Involvement'].astype(str)
mybar.bar(x_labels, job_involvement['Total Staff'],
          color='#050883', label='Total Staff')
myline = mybar.twinx()

myline.plot(x_labels,  job_involvement['Attrition Rate'],
            marker='v', color="#C20404", label='Attrited')
myline.set_ylabel('Attrition Rate (%)', fontname='Arial')
mybar.set_ylabel('Staff Count', fontname='Arial')
mybar.set_xlabel('Job Involvements', fontweight='bold', fontname='Arial')
plt.grid(axis='y', linestyle='dashed', alpha=0.5)
fig.legend(loc='upper right')
plt.title('Job Involvement', **title_font)
plt.tight_layout()
plt.show()

# overtime
overtime = attrition_tables('over_time')
overtime

fig, mybar = plt.subplots(figsize=(8, 6))
mybar.bar(overtime['Over_Time'], overtime['Total Staff'],
          color='#050883', label='Total Staff')
myline = mybar.twinx()

myline.plot(overtime['Over_Time'],  overtime['Attrition Rate'],
            marker='v', color="#C20404", label='Attrited')
myline.set_ylabel('Attrition Rate (%)', fontname='Arial')
mybar.set_ylabel('Staff Count', fontname='Arial')
mybar.set_xlabel('Overtime?', fontweight='bold', fontname='Arial')
plt.grid(axis='y', linestyle='dashed', alpha=0.5)
fig.legend(loc='upper right')
plt.title('Overtime and Attrtion', **title_font)
plt.tight_layout()
plt.show()
# business travel

business_travel = attrition_tables('business_travel')
business_travel

# create a fucntion for plotting line and bars


def double_plot(table_name, group_name, bar_x_label, plot_title):
    fig, mybar = plt.subplots(figsize=(8, 6))
    mybar.bar(table_name[group_name], table_name['Total Staff'],
              color='#050883', label='Total Staff')
    myline = mybar.twinx()

    myline.plot(table_name[group_name],  table_name['Attrition Rate'],
                marker='v', color="#C20404", label='Attrited')
    myline.set_ylabel('Attrition Rate (%)', fontname='Arial')
    mybar.set_ylabel('Staff Count', fontname='Arial')
    mybar.set_xlabel(bar_x_label, fontweight='bold',
                     fontname='Arial', labelpad=15)
    plt.grid(axis='y', linestyle='dashed', alpha=0.5)
    fig.legend(loc='upper right')
    plt.title(plot_title, **title_font)

    plt.tight_layout()
    plt.show()

    # salary range
salary_range = attrition_tables('salary_range')
salary_range
double_plot(salary_range, 'Salary_Range',
            'Salary Range', 'Salary and Attrition')
# distance from home
distance = attrition_tables('distance_from_home')
distance.sort_values(by='Distance_From_Home', ascending=True, inplace=True)
distance
# plot for distance from home and attriton rate
xlabels = distance['Distance_From_Home'].astype(str)
plt.figure(figsize=(8, 4))
plt.plot(xlabels, distance['Attrition Rate'], color='Blue')
# plt.plot(xlabels, distance['Total Staff'], color='Blue')
plt.title('Distance from home and attrition', **title_font)
plt.xlabel('Distance (km)')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()

# YEar since Last Promotion vs attrition.
last_promotion = attrition_tables('years_since_last_promotion').fillna(0)


last_promotion['Years_Since_Last_Promotion'] = last_promotion['Years_Since_Last_Promotion'].astype(
    str)
double_plot(last_promotion, 'Years_Since_Last_Promotion',
            'Years since last Promotion', 'Promotion tenure and Attrition')

# Tenure in company vs attrition

company_tenure = attrition_tables('years_at_company')
company_tenure['Years_At_Company'] = company_tenure['Years_At_Company'].astype(
    str)

company_tenure
company_tenure = company_tenure.dropna()
company_tenure

# years at company

plt.figure(figsize=(12, 6))
plt.bar(company_tenure['Years_At_Company'],
        company_tenure['Attrition Rate'], color='Blue')
plt.title('Years in Company vs Attrition', **title_font)
plt.ylabel("Attrition (%)")
plt.xlabel('Number of years')
plt.grid(axis='y', linestyle='dashed', alpha=.5)
plt.show()
double_plot(company_tenure, 'Years_At_Company',
            'Tenure in company (years)', 'Years in Company Vs Attrition')

# group the staff tenure into 4 groups

df['tenure_grp'] = pd.cut(
    df['years_at_company'],
    bins=[-1, 2, 7, 15, 50],
    labels=['Onboarding: below 2 years',
            'Established: 3-7 years',
            'Mid_Level: 8-15 years',
            'Long Term: 16years and above']
)
# TENURE

grouped_tenure = attrition_tables('tenure_grp')
grouped_tenure

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.bar(grouped_tenure['Tenure_Grp'],
        grouped_tenure['Total Staff'],
        color='#050883', label='Total Staff')
ax2 = ax1.twinx()
ax2.plot(grouped_tenure['Tenure_Grp'], grouped_tenure['Attrition Rate'],
         color='red', marker='o',
         linestyle='dashed', label='Attrition Rate')
ax1.set_xlabel('Tenure in company', labelpad=15, fontweight='bold')
ax1.set_ylabel('Staff Count', labelpad=15, fontweight='bold')
ax2.set_ylabel('Attrition Rate', labelpad=15, fontweight='bold')
fig.legend()
plt.title("Time spent in Company vs Attrition")
plt.tight_layout()
plt.show()
# ROLE
currrent_role_tenure = attrition_tables('years_in_current_role').sort_values(
    by='Attrited Staff', ascending=False).fillna(0)
currrent_role_tenure['Years_In_Current_Role'] = currrent_role_tenure['Years_In_Current_Role'].astype(
    str)
currrent_role_tenure

# GROUP INTO GRUPS OF YEARS IN CURRENT ROLE
df['role_tenure'] = pd.cut(
    df['years_in_current_role'],
    bins=[-1, 2, 5, 10, 50],
    labels=['New: below 2 years',
            'Mid: 3-5 years',
            'Experienced: 6-10 years',
            'Long Tenured: 11years and above']
)

role_tenure = attrition_tables('role_tenure')
role_tenure

# plot for number of years in current role and attrition
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.bar(role_tenure['Role_Tenure'],
        role_tenure['Total Staff'],
        color='#050883', label='Total Staff')
ax2 = ax1.twinx()
ax2.plot(role_tenure['Role_Tenure'], role_tenure['Attrition Rate'],
         color='red', marker='o',
         linestyle='dashed', label='Attrition Rate')
ax1.set_xlabel('Tenure in current role', labelpad=15, fontweight='bold')
ax1.set_ylabel('Staff Count', labelpad=15, fontweight='bold')
ax2.set_ylabel('Attrition Rate', labelpad=15, fontweight='bold')
fig.legend()
plt.title('Years in Current role vs Attrition', **title_font)
plt.tight_layout()
for exp in ax1.get_xticklabels():
    exp.set_rotation(15)

plt.show()

# comparing Salary and worklife balance scores

salary_table = df.groupby(['salary_range', 'work_life_balance']).agg(
    total=('employee_number', 'count'),
    attrited=('attrition', lambda x: (x == 'yes').sum())
).reset_index()

salary_table['attrition_rate'] = round(
    100 * salary_table['attrited'] / salary_table['total'], 2)

salary_table = salary_table.sort_values(by='attrition_rate', ascending=False)


salary_table

# create pivot table with salry grps and attriton rate and worklife balance
salary_pivot = salary_table.pivot(
    index='salary_range',
    columns='work_life_balance',
    values='attrition_rate'
)

salary_pivot

# plot
salary_pivot.plot(kind='bar', figsize=(10, 6), color=[
                  'red', 'orange', 'lightgreen', 'forestgreen'])

plt.title('Attrition Rate by Salary Group and Work-Life Balance',
          fontname='arial', fontweight='bold')
plt.ylabel('Attrition Rate (%)')
plt.xlabel('Salary Groups', labelpad=15, fontweight='bold')
plt.xticks(rotation=0)
plt.legend(title='Work Life Balance')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

overtime_js_table = df.groupby(['over_time', 'job_satisfaction']).agg(
    Total=('employee_number', 'count'),
    Attrition=('attrition', lambda x: (x == 'yes').sum())
).reset_index()

overtime_js_table['Attrition Rate'] = round((100 * overtime_js_table['Attrition'])
                                            / overtime_js_table['Total'], 2)

overtime_js_table['job_satisfaction'] = overtime_js_table['job_satisfaction'].astype(
    str)
overtime_js_table

overtime_js_pivot = overtime_js_table.pivot_table(index='over_time',
                                                  columns='job_satisfaction',
                                                  values='Attrition Rate')
overtime_js_pivot

overtime_js_pivot.plot(
    kind='bar', color=['red', 'orange', 'lightgreen', 'forestgreen'])
plt.title('Compare Overtime with Job Satisfaction', **title_font)
plt.xlabel('Ovetime Status', fontweight='bold')
plt.ylabel('Attrition Rate (%)')
plt.legend(title="Job Satisfaction")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=1)
plt.show()
