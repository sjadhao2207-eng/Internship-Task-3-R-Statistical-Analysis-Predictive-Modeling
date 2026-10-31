
# ============================================================
# WEEK 3: STATISTICAL ANALYSIS AND PREDICTIVE MODELING
# Dataset: Titanic Passenger Dataset
# Model: Logistic Regression
# Author: Sahil Jadhao
# ============================================================

# 1. LOAD LIBRARIES
library(tidyverse)
library(caret)
library(pROC)
library(car)

set.seed(123)

# 2. PROJECT PATHS
base_dir <- getwd()

output_graphs <- file.path(base_dir, "Outputs", "Graphs")
output_results <- file.path(base_dir, "Outputs", "Results")
output_models <- file.path(base_dir, "Outputs", "Models")

dir.create(output_graphs, recursive = TRUE, showWarnings = FALSE)
dir.create(output_results, recursive = TRUE, showWarnings = FALSE)
dir.create(output_models, recursive = TRUE, showWarnings = FALSE)

# 3. LOAD DATASET
data <- read.csv(
  file.path(base_dir, "Dataset", "titanic_train.csv"),
  stringsAsFactors = FALSE
)

cat("\n========== DATASET OVERVIEW ==========\n")
cat("Rows:", nrow(data), "\n")
cat("Columns:", ncol(data), "\n")

write.csv(
  data,
  file.path(output_results, "original_dataset_summary.csv"),
  row.names = FALSE
)

# 4. DATA CLEANING
cat("\n========== DATA CLEANING ==========\n")

# Convert survival into readable categories
data$Survived <- factor(
  data$Survived,
  levels = c(0, 1),
  labels = c("No", "Yes")
)

# Convert categorical variables into factors
data$Sex <- as.factor(data$Sex)
data$Pclass <- as.factor(data$Pclass)
data$Embarked <- as.factor(data$Embarked)

# Missing value summary
missing_summary <- data.frame(
  Variable = names(data),
  Missing_Values = colSums(is.na(data))
)

write.csv(
  missing_summary,
  file.path(output_results, "missing_values_summary.csv"),
  row.names = FALSE
)

print(missing_summary)

# Replace missing numerical values with median
data$Age[is.na(data$Age)] <- median(data$Age, na.rm = TRUE)
data$Fare[is.na(data$Fare)] <- median(data$Fare, na.rm = TRUE)

# Replace missing Embarked values with mode
mode_value <- names(which.max(table(data$Embarked)))
data$Embarked[is.na(data$Embarked)] <- mode_value

# Remove unnecessary columns
data <- data %>%
  select(-PassengerId, -Name, -Ticket, -Cabin)

cat("\nMissing values after cleaning:\n")
print(colSums(is.na(data)))

# 5. DESCRIPTIVE STATISTICS
cat("\n========== DESCRIPTIVE STATISTICS ==========\n")

summary_stats <- data %>%
  summarise(
    Total_Passengers = n(),
    Mean_Age = mean(Age),
    Median_Age = median(Age),
    SD_Age = sd(Age),
    Mean_Fare = mean(Fare),
    Median_Fare = median(Fare),
    SD_Fare = sd(Fare),
    Survival_Rate = mean(Survived == "Yes") * 100
  )

print(summary_stats)

write.csv(
  summary_stats,
  file.path(output_results, "descriptive_statistics.csv"),
  row.names = FALSE
)

# 6. DISTRIBUTION ANALYSIS

# Age distribution
p1 <- ggplot(data, aes(x = Age)) +
  geom_histogram(bins = 30, fill = "steelblue", color = "white") +
  labs(
    title = "Distribution of Passenger Age",
    x = "Age",
    y = "Number of Passengers"
  ) +
  theme_minimal()

ggsave(
  file.path(output_graphs, "01_age_distribution.png"),
  p1, width = 8, height = 5
)

# Fare distribution
p2 <- ggplot(data, aes(x = Fare)) +
  geom_histogram(bins = 30, fill = "darkgreen", color = "white") +
  labs(
    title = "Distribution of Passenger Fare",
    x = "Fare",
    y = "Frequency"
  ) +
  theme_minimal()

ggsave(
  file.path(output_graphs, "02_fare_distribution.png"),
  p2, width = 8, height = 5
)

# 7. NORMALITY TESTING
cat("\n========== NORMALITY TESTING ==========\n")

age_normality <- shapiro.test(data$Age)
fare_normality <- shapiro.test(data$Fare)

normality_results <- data.frame(
  Variable = c("Age", "Fare"),
  W_Statistic = c(
    unname(age_normality$statistic),
    unname(fare_normality$statistic)
  ),
  P_Value = c(
    age_normality$p.value,
    fare_normality$p.value
  )
)

print(normality_results)

write.csv(
  normality_results,
  file.path(output_results, "normality_test_results.csv"),
  row.names = FALSE
)

# 8. CORRELATION ANALYSIS
cat("\n========== CORRELATION ANALYSIS ==========\n")

correlation_test <- cor.test(
  data$Age,
  data$Fare,
  method = "spearman"
)

cat("Spearman correlation:", correlation_test$estimate, "\n")
cat("P-value:", correlation_test$p.value, "\n")

correlation_results <- data.frame(
  Variables = "Age and Fare",
  Correlation = unname(correlation_test$estimate),
  P_Value = correlation_test$p.value
)

write.csv(
  correlation_results,
  file.path(output_results, "correlation_results.csv"),
  row.names = FALSE
)

# 9. HYPOTHESIS TESTING

cat("\n========== HYPOTHESIS TESTING ==========\n")

# Test 1: Association between gender and survival
# H0: Gender and survival are independent.
# H1: Gender and survival are associated.

gender_table <- table(data$Sex, data$Survived)

gender_test <- chisq.test(gender_table, correct = FALSE)

cat("\nChi-square test: Gender vs Survival\n")
print(gender_test)

# Test 2: Age difference between survivors and non-survivors
# H0: Age distributions are equal.
# H1: Age distributions are different.

age_test <- wilcox.test(Age ~ Survived, data = data)

cat("\nWilcoxon test: Age vs Survival\n")
print(age_test)

hypothesis_results <- data.frame(
  Test = c(
    "Chi-square: Gender vs Survival",
    "Wilcoxon: Age vs Survival"
  ),
  Statistic = c(
    unname(gender_test$statistic),
    unname(age_test$statistic)
  ),
  P_Value = c(
    gender_test$p.value,
    age_test$p.value
  )
)

write.csv(
  hypothesis_results,
  file.path(output_results, "hypothesis_test_results.csv"),
  row.names = FALSE
)

# 10. PREPARE MODELING DATA

model_data <- data %>%
  select(
    Survived,
    Pclass,
    Sex,
    Age,
    Fare,
    SibSp,
    Parch,
    Embarked
  )

model_data <- droplevels(model_data)

# 11. TRAIN-TEST SPLIT (80:20)

cat("\n========== TRAIN-TEST SPLIT ==========\n")

train_index <- createDataPartition(
  model_data$Survived,
  p = 0.80,
  list = FALSE
)

train_data <- model_data[train_index, ]
test_data <- model_data[-train_index, ]

cat("Training rows:", nrow(train_data), "\n")
cat("Testing rows:", nrow(test_data), "\n")

# 12. FIVE-FOLD CROSS-VALIDATION

cat("\n========== CROSS VALIDATION ==========\n")

control <- trainControl(
  method = "cv",
  number = 5
)

# 13. LOGISTIC REGRESSION MODEL

cat("\n========== LOGISTIC REGRESSION ==========\n")

model <- train(
  Survived ~ .,
  data = train_data,
  method = "glm",
  family = binomial(),
  trControl = control,
  metric = "Accuracy"
)

print(model)

# Save model
saveRDS(
  model,
  file.path(output_models, "logistic_regression_model.rds")
)

# 14. PREDICTIONS

predicted_class <- predict(model, newdata = test_data)

predicted_probability <- predict(
  model,
  newdata = test_data,
  type = "prob"
)[, "Yes"]

# 15. CONFUSION MATRIX

cat("\n========== CONFUSION MATRIX ==========\n")

confusion <- confusionMatrix(
  predicted_class,
  test_data$Survived,
  positive = "Yes"
)

print(confusion)

# 16. PERFORMANCE METRICS

accuracy <- as.numeric(confusion$overall["Accuracy"])
precision <- as.numeric(confusion$byClass["Precision"])
recall <- as.numeric(confusion$byClass["Recall"])
f1 <- as.numeric(confusion$byClass["F1"])

roc_object <- roc(
  response = test_data$Survived,
  predictor = predicted_probability,
  levels = c("No", "Yes"),
  direction = "<",
  quiet = TRUE
)

auc_value <- as.numeric(auc(roc_object))

performance <- data.frame(
  Metric = c(
    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "ROC-AUC"
  ),
  Value = c(
    accuracy,
    precision,
    recall,
    f1,
    auc_value
  )
)

cat("\n========== MODEL PERFORMANCE ==========\n")
print(performance)

write.csv(
  performance,
  file.path(output_results, "model_performance.csv"),
  row.names = FALSE
)

# 17. CONFUSION MATRIX VISUALIZATION

confusion_data <- as.data.frame(confusion$table)

p3 <- ggplot(
  confusion_data,
  aes(x = Reference, y = Prediction, fill = Freq)
) +
  geom_tile(color = "white") +
  geom_text(aes(label = Freq), size = 7) +
  scale_fill_gradient(low = "lightblue", high = "darkblue") +
  labs(
    title = "Confusion Matrix - Logistic Regression",
    x = "Actual Outcome",
    y = "Predicted Outcome"
  ) +
  theme_minimal()

ggsave(
  file.path(output_graphs, "03_confusion_matrix.png"),
  p3, width = 7, height = 5
)

# 18. ROC CURVE

roc_data <- data.frame(
  Specificity = roc_object$specificities,
  Sensitivity = roc_object$sensitivities
)

p4 <- ggplot(
  roc_data,
  aes(x = 1 - Specificity, y = Sensitivity)
) +
  geom_line(color = "blue", linewidth = 1.2) +
  geom_abline(
    intercept = 0,
    slope = 1,
    linetype = "dashed"
  ) +
  labs(
    title = paste("ROC Curve - AUC:", round(auc_value, 3)),
    x = "False Positive Rate",
    y = "True Positive Rate"
  ) +
  theme_minimal()

ggsave(
  file.path(output_graphs, "04_roc_curve.png"),
  p4, width = 7, height = 5
)

# 19. MODEL DIAGNOSTICS

cat("\n========== MODEL DIAGNOSTICS ==========\n")

final_glm <- model$finalModel

# Residuals vs fitted plot
diagnostic_data <- data.frame(
  Fitted = fitted(final_glm),
  Deviance_Residuals = residuals(
    final_glm,
    type = "deviance"
  )
)

p5 <- ggplot(
  diagnostic_data,
  aes(x = Fitted, y = Deviance_Residuals)
) +
  geom_point(alpha = 0.6) +
  geom_hline(
    yintercept = 0,
    linetype = "dashed",
    color = "red"
  ) +
  labs(
    title = "Residuals vs Fitted Values",
    x = "Fitted Values",
    y = "Deviance Residuals"
  ) +
  theme_minimal()

ggsave(
  file.path(output_graphs, "05_residual_diagnostic.png"),
  p5, width = 7, height = 5
)

# Q-Q plot of deviance residuals
qq_data <- data.frame(
  Theoretical = qnorm(ppoints(length(residuals(final_glm)))),
  Sample = sort(residuals(final_glm, type = "deviance"))
)

p6 <- ggplot(
  qq_data,
  aes(x = Theoretical, y = Sample)
) +
  geom_point(alpha = 0.6) +
  geom_abline(
    intercept = 0,
    slope = 1,
    color = "red"
  ) +
  labs(
    title = "Q-Q Plot of Deviance Residuals",
    x = "Theoretical Quantiles",
    y = "Sample Quantiles"
  ) +
  theme_minimal()

ggsave(
  file.path(output_graphs, "06_qq_plot.png"),
  p6, width = 7, height = 5
)

# 20. MULTICOLLINEARITY CHECK

cat("\n========== MULTICOLLINEARITY ==========\n")

vif_results <- tryCatch(
  car::vif(final_glm),
  error = function(e) {
    cat("VIF could not be calculated:", e$message, "\n")
    NULL
  }
)

if (!is.null(vif_results)) {
  print(vif_results)

  vif_table <- data.frame(
    Variable = names(vif_results),
    VIF = as.numeric(vif_results)
  )

  write.csv(
    vif_table,
    file.path(output_results, "vif_results.csv"),
    row.names = FALSE
  )
}

# 21. LOGISTIC REGRESSION COEFFICIENTS

coefficient_results <- as.data.frame(
  summary(final_glm)$coefficients
)

coefficient_results$Variable <- rownames(coefficient_results)
coefficient_results$Odds_Ratio <- exp(coefficient_results$Estimate)

write.csv(
  coefficient_results,
  file.path(output_results, "logistic_coefficients.csv"),
  row.names = FALSE
)

# 22. FINAL SUMMARY

cat("\n========================================\n")
cat("WEEK 3 ANALYSIS COMPLETED SUCCESSFULLY\n")
cat("========================================\n")

cat("Dataset rows:", nrow(data), "\n")
cat("Training rows:", nrow(train_data), "\n")
cat("Testing rows:", nrow(test_data), "\n")
cat("Cross-validation: 5-fold\n")
cat("Model: Logistic Regression\n")
cat("Accuracy:", round(accuracy * 100, 2), "%\n")
cat("Precision:", round(precision, 3), "\n")
cat("Recall:", round(recall, 3), "\n")
cat("F1 Score:", round(f1, 3), "\n")
cat("ROC-AUC:", round(auc_value, 3), "\n")

cat("\nGraphs saved in:", output_graphs, "\n")
cat("Results saved in:", output_results, "\n")
cat("Model saved in:", output_models, "\n")

cat("\n========================================\n")
