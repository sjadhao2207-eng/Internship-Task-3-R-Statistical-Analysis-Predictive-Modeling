
import os
import csv
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ==========================================================
# WEEK 3 REPORT: STATISTICAL ANALYSIS AND PREDICTIVE MODELING
# Author: Sahil Jadhao
# ==========================================================

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GRAPH_DIR = os.path.join(BASE, "Outputs", "Graphs")
RESULT_DIR = os.path.join(BASE, "Outputs", "Results")
MODEL_DIR = os.path.join(BASE, "Outputs", "Models")
R_SCRIPT = os.path.join(BASE, "R_Scripts", "week3_analysis.R")

OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "Week_3_Statistical_Analysis_Report.docx"
)

doc = Document()

# Page setup
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Fonts and styles
styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(10)

styles["Heading 1"].font.name = "Calibri"
styles["Heading 1"].font.color.rgb = RGBColor(31, 78, 121)

styles["Heading 2"].font.name = "Calibri"
styles["Heading 2"].font.color.rgb = RGBColor(46, 116, 181)

def paragraph(text, bold=False):
    p = doc.add_paragraph()
    r = p.add_run(str(text))
    r.bold = bold
    return p

def bullet(text):
    doc.add_paragraph(str(text), style="List Bullet")

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Light Shading Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = str(header)

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)

    for row in table.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    return table

def read_csv(filename):
    path = os.path.join(RESULT_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def add_graph(filename, heading, explanation, interpretation):
    doc.add_heading(heading, level=2)
    paragraph(explanation)

    path = os.path.join(GRAPH_DIR, filename)

    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Inches(5.8))
    else:
        paragraph("Image not available: " + filename)

    paragraph("Interpretation: " + interpretation)

def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run("Page ")

    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)

# ==========================================================
# COVER PAGE
# ==========================================================

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(100)

r = p.add_run("WEEK 3 INTERNSHIP REPORT")
r.bold = True
r.font.size = Pt(25)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(
    "\nSTATISTICAL ANALYSIS AND\nPREDICTIVE MODELING USING R"
)
r.bold = True
r.font.size = Pt(19)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\nTitanic Passenger Survival Prediction").font.size = Pt(15)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\nSubmitted by\n").bold = True
p.add_run("Sahil Jadhao\n")
p.add_run("Virtual R Data Analyst Internship\n")
p.add_run("Week 3 Task\n")
p.add_run("Tools: R, Visual Studio Code, Logistic Regression")

doc.add_page_break()

# ==========================================================
# ABSTRACT
# ==========================================================

doc.add_heading("Abstract", level=1)

paragraph(
    "This project focuses on statistical analysis and predictive "
    "modeling using the R programming language. The Titanic passenger "
    "dataset is used to investigate relationships between passenger "
    "characteristics and survival outcomes."
)

paragraph(
    "Statistical techniques include descriptive statistics, "
    "normality testing, Spearman correlation, Chi-square testing, "
    "and the Wilcoxon rank-sum test. A Logistic Regression "
    "classification model is developed to predict passenger survival. "
    "The model is evaluated using a training-testing split, five-fold "
    "cross-validation, confusion matrix, and classification metrics."
)

# ==========================================================
# OBJECTIVES
# ==========================================================

doc.add_heading("1. Objectives", level=1)

objectives = [
    "Identify and prepare a suitable public dataset.",
    "Perform exploratory statistical analysis.",
    "Examine numerical variable distributions and correlations.",
    "Formulate and test statistical hypotheses.",
    "Develop a Logistic Regression classification model.",
    "Apply five-fold cross-validation.",
    "Evaluate model performance using classification metrics.",
    "Analyze model diagnostics and identify possible improvements."
]

for item in objectives:
    bullet(item)

# ==========================================================
# DATASET
# ==========================================================

doc.add_heading("2. Dataset Identification and Overview", level=1)

paragraph(
    "The Titanic training dataset was selected because it contains "
    "passenger characteristics and a binary survival outcome. "
    "This makes it suitable for statistical analysis and binary "
    "classification."
)

add_table(
    ["Dataset property", "Details"],
    [
        ["Dataset", "Titanic passenger training dataset"],
        ["Original observations", "891"],
        ["Original variables", "12"],
        ["Target variable", "Survived"],
        ["Prediction type", "Binary classification"],
        ["Model", "Logistic Regression"]
    ]
)

paragraph("Important variables used in the model:")

add_table(
    ["Variable", "Description"],
    [
        ["Survived", "Target: No or Yes"],
        ["Pclass", "Passenger ticket class"],
        ["Sex", "Passenger gender category"],
        ["Age", "Passenger age"],
        ["Fare", "Ticket fare"],
        ["SibSp", "Siblings or spouses aboard"],
        ["Parch", "Parents or children aboard"],
        ["Embarked", "Port of embarkation"]
    ]
)

# ==========================================================
# DATA PREPARATION
# ==========================================================

doc.add_heading("3. Data Cleaning and Preparation", level=1)

paragraph(
    "The original dataset contains 891 observations and 12 variables. "
    "The Age variable has 177 missing values. Missing Age and Fare "
    "values were replaced with their respective medians. Missing "
    "Embarked values were intended to be replaced with the most "
    "frequent category."
)

paragraph(
    "PassengerId, Name, Ticket, and Cabin were excluded from the "
    "predictive model. The Survived variable was converted into a "
    "factor with two classes: No and Yes. Categorical predictors "
    "were converted into factors."
)

paragraph(
    "The cleaned modeling dataset contains eight variables, "
    "including the survival target and seven predictors."
)

# ==========================================================
# DESCRIPTIVE STATISTICS
# ==========================================================

doc.add_heading("4. Exploratory Statistical Analysis", level=1)

paragraph(
    "Descriptive statistics were calculated to understand the "
    "distribution and central tendency of numerical variables."
)

add_table(
    ["Statistic", "Observed result"],
    [
        ["Total passengers", "891"],
        ["Mean age", "29.36 years"],
        ["Median age", "28 years"],
        ["Age standard deviation", "13.02"],
        ["Mean fare", "32.20"],
        ["Median fare", "14.45"],
        ["Fare standard deviation", "49.69"],
        ["Overall survival rate", "38.38%"]
    ]
)

# ==========================================================
# DISTRIBUTION AND NORMALITY
# ==========================================================

doc.add_heading("5. Distribution and Normality Testing", level=1)

paragraph(
    "The Shapiro-Wilk test was applied to Age and Fare to examine "
    "whether their distributions were consistent with normality."
)

add_table(
    ["Variable", "W statistic", "P-value", "Interpretation"],
    [
        ["Age", "0.9541", "4.65 × 10⁻¹⁶",
         "Evidence against normality"],
        ["Fare", "0.5219", "1.08 × 10⁻⁴³",
         "Evidence against normality"]
    ]
)

paragraph(
    "At the 5% significance level, both p-values are below 0.05. "
    "Therefore, the null hypothesis of normality is rejected for "
    "both variables. The tests are sensitive to sample size, so "
    "histograms and other graphical evidence should also be considered."
)

add_graph(
    "01_age_distribution.png",
    "5.1 Passenger Age Distribution",
    "The histogram shows the frequency distribution of passenger ages.",
    "It helps identify the concentration and spread of passenger ages. "
    "The median age used for missing-value replacement was 28 years."
)

add_graph(
    "02_fare_distribution.png",
    "5.2 Passenger Fare Distribution",
    "The histogram displays the distribution of passenger ticket fares.",
    "The fare distribution is strongly non-normal and includes "
    "substantial variation between passengers."
)

# ==========================================================
# CORRELATION
# ==========================================================

doc.add_heading("6. Correlation Analysis", level=1)

paragraph(
    "Spearman rank correlation was used to examine the relationship "
    "between passenger age and fare. This method is suitable for "
    "assessing monotonic association without requiring normally "
    "distributed variables."
)

add_table(
    ["Variables", "Spearman correlation", "P-value", "Interpretation"],
    [
        ["Age and Fare", "0.1260", "0.000163",
         "Weak positive association"]
    ]
)

paragraph(
    "The result indicates a weak positive association between Age "
    "and Fare. The warning about ties means an exact p-value was "
    "not calculated; the reported p-value is an approximation."
)

# ==========================================================
# HYPOTHESIS TESTING
# ==========================================================

doc.add_heading("7. Hypothesis Testing", level=1)

doc.add_heading("7.1 Chi-square Test: Gender and Survival", level=2)

paragraph(
    "Null hypothesis (H0): Gender and passenger survival are independent."
)

paragraph(
    "Alternative hypothesis (H1): Gender and passenger survival "
    "are associated."
)

paragraph(
    "The Chi-square test produced a statistic of 263.05 with one "
    "degree of freedom and a p-value below 2.2 × 10⁻¹⁶."
)

paragraph(
    "Since the p-value is below 0.05, the null hypothesis is rejected. "
    "There is strong statistical evidence of an association between "
    "gender and survival in this dataset."
)

doc.add_heading("7.2 Wilcoxon Test: Age and Survival", level=2)

paragraph(
    "Null hypothesis (H0): The age distributions of survivors and "
    "non-survivors have the same location."
)

paragraph(
    "Alternative hypothesis (H1): The age distributions have "
    "different locations."
)

paragraph(
    "The Wilcoxon rank-sum test produced W = 97,979 and p = 0.2697. "
    "At the 5% significance level, the null hypothesis is not rejected. "
    "This test did not detect a statistically significant location "
    "difference between the two age distributions."
)

# ==========================================================
# MODEL BUILDING
# ==========================================================

doc.add_heading("8. Predictive Model Development", level=1)

paragraph(
    "Logistic Regression was selected because the target variable "
    "Survived has two categories: No and Yes. The model estimates "
    "the probability of survival using passenger characteristics."
)

paragraph(
    "The predictors used were passenger class, sex, age, fare, "
    "number of siblings or spouses, number of parents or children, "
    "and embarkation port."
)

doc.add_heading("8.1 Training and Testing Split", level=2)

add_table(
    ["Dataset portion", "Observations", "Percentage"],
    [
        ["Training data", "714", "80%"],
        ["Testing data", "177", "20%"]
    ]
)

paragraph(
    "The dataset was divided into training and testing subsets "
    "using an 80:20 split. A fixed random seed was used for "
    "reproducibility."
)

doc.add_heading("8.2 Five-Fold Cross-Validation", level=2)

paragraph(
    "Five-fold cross-validation was configured on the training data. "
    "The training observations were divided into five folds, with "
    "each fold used for validation in turn."
)

paragraph(
    "The cross-validation accuracy was approximately 79.97%. "
    "This provides an estimate of model performance across different "
    "training and validation partitions."
)

# ==========================================================
# MODEL PERFORMANCE
# ==========================================================

doc.add_heading("9. Model Evaluation", level=1)

paragraph(
    "The trained Logistic Regression model was evaluated on the "
    "177 observations in the testing dataset."
)

add_table(
    ["Metric", "Result"],
    [
        ["Accuracy", "79.10%"],
        ["Precision", "74.60%"],
        ["Recall / Sensitivity", "69.12%"],
        ["F1-score", "71.76%"],
        ["ROC-AUC", "84.09%"],
        ["Specificity", "85.32%"],
        ["Balanced accuracy", "77.22%"]
    ]
)

paragraph(
    "The model achieved 79.10% test accuracy and an ROC-AUC of "
    "0.841. The ROC-AUC indicates useful discrimination between "
    "the two survival classes. Precision of 74.60% means that "
    "approximately 74.6% of predicted survivors were actual survivors. "
    "Recall of 69.12% indicates that the model identified approximately "
    "69.1% of actual survivors."
)

# ==========================================================
# CONFUSION MATRIX
# ==========================================================

doc.add_heading("10. Confusion Matrix", level=1)

add_table(
    ["Prediction", "Actual No", "Actual Yes"],
    [
        ["Predicted No", "93", "21"],
        ["Predicted Yes", "16", "47"]
    ]
)

paragraph(
    "The model correctly classified 93 non-survivors and 47 survivors. "
    "It incorrectly classified 16 non-survivors as survivors and "
    "21 survivors as non-survivors. Overall, 140 out of 177 test "
    "observations were classified correctly."
)

add_graph(
    "03_confusion_matrix.png",
    "10.1 Confusion Matrix Visualization",
    "The confusion matrix compares actual survival outcomes with "
    "predicted outcomes.",
    "The diagonal cells represent correct predictions, while the "
    "off-diagonal cells represent classification errors."
)

# ==========================================================
# ROC CURVE
# ==========================================================

doc.add_heading("11. ROC Curve Analysis", level=1)

add_graph(
    "04_roc_curve.png",
    "11.1 Receiver Operating Characteristic Curve",
    "The ROC curve plots the true positive rate against the false "
    "positive rate at different classification thresholds.",
    "The model achieved an AUC of approximately 0.841, indicating "
    "good ability to distinguish between survivors and non-survivors."
)

# ==========================================================
# DIAGNOSTICS
# ==========================================================

doc.add_heading("12. Model Diagnostics", level=1)

add_graph(
    "05_residual_diagnostic.png",
    "12.1 Deviance Residuals vs Fitted Values",
    "This plot examines residual patterns against fitted probabilities.",
    "It can help identify unusual residual patterns and observations "
    "that may deserve further investigation."
)

add_graph(
    "06_qq_plot.png",
    "12.2 Q-Q Plot of Deviance Residuals",
    "The Q-Q plot compares ordered deviance residuals with theoretical "
    "normal quantiles.",
    "It provides a visual diagnostic, but normality of residuals is "
    "not a requirement for logistic regression."
)

paragraph(
    "The initial model run produced a rank-deficient fit warning. "
    "This indicates that some model coefficients may not be uniquely "
    "estimated, potentially because of redundant or empty factor "
    "levels. VIF calculation also failed because of aliased "
    "coefficients. These issues should be investigated before "
    "treating all individual coefficients as reliable."
)

# ==========================================================
# STRENGTHS AND LIMITATIONS
# ==========================================================

doc.add_heading("13. Model Strengths", level=1)

for item in [
    "Logistic Regression is appropriate for a binary target variable.",
    "The model achieved 79.10% accuracy on the test dataset.",
    "The ROC-AUC of 0.841 indicates useful classification ability.",
    "Five-fold cross-validation was used to assess training performance.",
    "Multiple evaluation metrics were used rather than accuracy alone."
]:
    bullet(item)

doc.add_heading("14. Limitations and Potential Improvements", level=1)

for item in [
    "Investigate rank-deficient coefficients and factor levels.",
    "Check blank strings as well as NA values during missing-value handling.",
    "Use stratified repeated cross-validation for more stable estimates.",
    "Compare Logistic Regression with Random Forest and other classifiers.",
    "Consider feature selection and regularization.",
    "Evaluate probability calibration and alternative classification thresholds.",
    "Investigate class imbalance and compare balanced performance metrics.",
    "Use additional data or external validation to test generalization."
]:
    bullet(item)

# ==========================================================
# CONCLUSION
# ==========================================================

doc.add_heading("15. Conclusion", level=1)

paragraph(
    "This project applied statistical analysis and predictive modeling "
    "to the Titanic passenger dataset using R. Descriptive statistics, "
    "normality testing, correlation analysis, and hypothesis testing "
    "were used to explore the data."
)

paragraph(
    "A Logistic Regression classifier was developed with an 80:20 "
    "training-testing split and five-fold cross-validation. The model "
    "achieved 79.10% test accuracy, 71.76% F1-score, and 84.09% ROC-AUC."
)

paragraph(
    "The results demonstrate how statistical methods and classification "
    "models can be used to investigate patterns and make predictions. "
    "The model also has limitations, including a rank-deficiency "
    "warning that requires further investigation. Future work can "
    "improve the model through data-quality checks, feature selection, "
    "regularization, and comparison with other classification methods."
)

# ==========================================================
# APPENDIX: COMPLETE R SOURCE CODE
# ==========================================================

doc.add_page_break()
doc.add_heading("16. Appendix: Complete R Source Code", level=1)

paragraph(
    "The following appendix contains the R script used to perform "
    "the statistical analysis, hypothesis testing, model development, "
    "and evaluation."
)

if os.path.exists(R_SCRIPT):
    with open(R_SCRIPT, "r", encoding="utf-8") as f:
        code_text = f.read()

    for line in code_text.splitlines():
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1
        r = p.add_run(line if line else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(7)
else:
    paragraph("R source code file was not found.")

# ==========================================================
# FOOTERS
# ==========================================================

for section in doc.sections:
    footer = section.footer.paragraphs[0]
    footer.add_run(
        "Week 3 Statistical Analysis and Predictive Modeling | Sahil Jadhao"
    )
    add_page_number(footer)

# ==========================================================
# SAVE REPORT
# ==========================================================

doc.save(OUTPUT_FILE)

print("\n==========================================")
print("WEEK 3 REPORT GENERATED SUCCESSFULLY")
print("==========================================")
print("Report:", OUTPUT_FILE)
print("Statistical analysis: Included")
print("Hypothesis testing: Included")
print("Logistic Regression: Included")
print("Model metrics: Included")
print("Diagnostic graphs: Included")
print("R source code appendix: Included")
print("==========================================")
