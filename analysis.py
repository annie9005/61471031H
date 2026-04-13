import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
import plotly.express as px
import os

# Create plots directory if not exists
if not os.path.exists("plots"):
    os.makedirs("plots")

def run_ancova_full(df_wide, outcome_post, outcome_pre):
    df_clean = df_wide[[outcome_post, 'group', outcome_pre]].dropna()
    model = smf.ols(f"{outcome_post} ~ group + {outcome_pre}", data=df_clean).fit()
    table = anova_lm(model, typ=2)
    f_val = table.loc['group', 'F']
    p_val = table.loc['group', 'PR(>F)']
    ss_effect = table.loc['group', 'sum_sq']
    ss_resid = table.loc['Residual', 'sum_sq']
    eta2_p = ss_effect / (ss_effect + ss_resid)
    return f_val, p_val, eta2_p

def plot_interaction(df_long, outcome):
    name_map = {
        "motivation": "Learning Motivation",
        "il": "Intrinsic Load",
        "el": "Extraneous Load",
        "gl": "Germane Load"
    }
    full_name = name_map.get(outcome, outcome)
    summary = df_long.groupby(['group', 'time'])[outcome].agg(['mean', 'std', 'count']).reset_index()
    summary['se'] = summary['std'] / np.sqrt(summary['count'])
    summary['time'] = pd.Categorical(summary['time'], categories=["pre", "post"], ordered=True)
    summary = summary.sort_values(['group', 'time'])
    fig = px.line(
        summary, x="time", y="mean", color="group", error_y="se", markers=True,
        title=f"Interaction Effect of {full_name}",
        labels={"mean": f"Average {full_name} Score", "time": "Time Point", "group": "Group"},
        template="plotly_white", line_dash="group"
    )
    safe_name = full_name.replace(" ", "_").lower()
    file_path = f"plots/{safe_name}_interaction.png"
    fig.write_image(file_path)
    print(f"Updated plot: {file_path}")

def generate_academic_table(df_wide):
    def get_stats(group_name, col):
        subset = df_wide[df_wide['group'] == group_name][col]
        return subset.mean(), subset.std()

    sections = [
        ("Learning Motivation", [
            ("pretest", "motivation_pre", "motivation_pre"),
            ("posttest", "motivation_post", "motivation_pre")
        ]),
        ("Cognitive Load", [
            ("intrinsic load", "il_post", "il_pre"),
            ("extraneous load", "el_post", "el_pre"),
            ("germane load", "gl_post", "gl_pre")
        ])
    ]

    latex_code = r"""
% Needs \usepackage{booktabs}
\begin{table}[htbp]
\centering
\caption{Descriptive statistics for learning motivation and cognitive load}
\label{tab:academic_results}
\begin{tabular}{lcccccccc}
\toprule
 & \multicolumn{2}{c}{EG ($N=53$)} & \multicolumn{2}{c}{CG ($N=53$)} & $F$ & $p$ & $\eta^2$ \\
\cmidrule(lr){2-3} \cmidrule(lr){4-5}
Variable & Mean & SD & Mean & SD & & & \\
\midrule
"""
    for section_name, vars in sections:
        latex_code += f"\\textbf{{{section_name}}} & & & & & & & \\\\\n"
        for label, post_col, pre_col in vars:
            eg_m, eg_sd = get_stats('Exp', post_col)
            cg_m, cg_sd = get_stats('Ctrl', post_col)
            if label == "pretest":
                f_str, p_str, eta_str = "-", "-", "-"
            else:
                f, p, e2 = run_ancova_full(df_wide, post_col, pre_col)
                f_str, p_str, eta_str = f"{f:.2f}", f"{p:.3f}", f"{e2:.2f}"
            latex_code += f"\\quad {label} & {eg_m:.2f} & {eg_sd:.2f} & {cg_m:.2f} & {cg_sd:.2f} & {f_str} & {p_str} & {eta_str} \\\\\n"
    latex_code += r"""\bottomrule
\end{tabular}
\end{table}
"""
    with open("academic_table.tex", "w", encoding="utf-8") as f:
        f.write(latex_code)
    print("Generated academic_table.tex")

if __name__ == "__main__":
    if os.path.exists("data_wide.csv") and os.path.exists("data_long.csv"):
        df_wide = pd.read_csv("data_wide.csv")
        df_long = pd.read_csv("data_long.csv")
        
        # 1. Update Table
        generate_academic_table(df_wide)
        
        # 2. Update Plots
        for outcome in ["motivation", "il", "el", "gl"]:
            plot_interaction(df_long, outcome)
        
        print("Final analysis complete. Plots and Table are synchronized.")
