Image /page/0/Picture/0 description: The image is a digital rendering of a network of interconnected nodes and lines, set against a dark blue background. The nodes are represented by glowing, hexagonal shapes with intricate patterns inside, suggesting a high-tech or futuristic theme. The lines connecting the nodes are thin and luminous, creating a sense of flow and connectivity. There are also numerous small, bright dots scattered throughout the image, adding to the overall impression of a complex and dynamic system. The color palette is dominated by shades of blue, with the glowing elements providing contrast and visual interest.

Accuracy Metrics in Machine Learning: Types and Examples

This presentation explores essential evaluation metrics in machine learning. Understanding these metrics is crucial for effective model assessment. We will cover various types and their applications.

Image /page/1/Picture/2 description: A blurry, circular image shows a man wearing sunglasses and a suit. He is standing in front of a blue car.

by abinash panta

Image /page/2/Picture/0 description: The image shows a close-up of a magnifying glass over a digital display of a world map and a line graph. The graph is white and jagged, with peaks and valleys, and it overlays the map. The map is pixelated and blue, with the continents visible. The magnifying glass has a black frame and is slightly out of focus. The background is a dark blue color, and there are some other graphs and numbers visible in the background, but they are out of focus.

Why Do Metrics Matter?

Model Selection

Metrics guide choosing the best model for a task.

Image /page/3/Picture/4 description: The image shows a gear icon with angle brackets and a forward slash inside. The angle brackets and forward slash are meant to represent code.

Performance Insight

They reveal how well a model is actually performing.

Image /page/3/Picture/7 description: The image shows a simple line drawing of a balance scale. The scale has two pans suspended from a central beam that is supported by a vertical stand. The pans are empty and appear to be balanced.

Task Alignment

Different metrics suit classification vs. regression tasks.

Metrics are vital for both selecting and continuously improving machine learning models. The choice of metric depends heavily on the specific machine learning task.

## Confusion Matrix

Image /page/4/Figure/1 description: The image shows a 2x2 grid with the following labels: True Positive, False Positive, False, and True. There are checkmarks and an X on the left side of the grid.

Confusion Matrix: Foundation for Classification Metrics

Actual Spam (20)

Predicted Spam

Predicted Non-Spam

True Positive (TP)

15 (correctly spam)

5 (missed spam)

Actual Non-Spam (80)

5 (false alarm)

75 (correctly non-spam)

A 2x2 table, the confusion matrix, is fundamental for binary classification. It organizes predictions into True Positives, False Positives, True Negatives, and False Negatives. For example, consider 100 emails: 80 non-spam and 20 spam.

Image /page/6/Picture/0 description: The image shows a bar graph with four bars of increasing height. The bars are all shades of blue, with the tallest bar having the text 's.18%' on it in white.

Accuracy: The Basic Metric

85%

Email Prediction Accuracy

Overall correct predictions on 100 emails.

70

Non-Spam Correct

Emails correctly identified as non-spam.

15

Spam Correct

Emails correctly identified as spam.

Accuracy measures the proportion of correctly classified instances: (TP + TN) / Total. For example, 85% accuracy on 100 emails (70 non-spam, 15 spam predicted right). It is best used when classes are well-balanced.

Image /page/8/Picture/0 description: The image shows a blue and white target with a blue arrow in the center. The target has concentric circles of blue and white, and the arrow is pointing directly at the bullseye. There are also some light blue circles in the background.

## Precision: Focus on Positive Predictions

Image /page/9/Picture/1 description: The image shows a white chevron pointing downwards. Inside the chevron is a dark blue icon of a closed envelope.

18 Emails Tagged Spam

Total emails the filter marked as spam.

Image /page/9/Picture/4 description: The image shows a check mark symbol in dark blue against a light blue background. The background is shaped like a chevron, with the point facing downwards.

15 Really Spam

Number of actual spam emails among those marked.

Image /page/10/Picture/0 description: The image shows a white chevron with a gray border. Inside the chevron is a dark blue percent sign.

Precision ≈ 83%

15 true spam out of 18 predicted spam.

Precision calculates TP / (TP + FP). It evaluates the accuracy of positive predictions. A spam filter marking 18 emails as spam, with 15 being true spam, yields ~83% precision. This metric is crucial when false positives are costly, such as in medical diagnoses.

Recall (Sensitivity): Identifying True Positives

Total Actual Spam

20 emails were genuinely spam.

Detected Spam

15 of these 20 were correctly identified.

Recall Calculation

15 True Positives / 20 Actual Positives = 75%.

Recall, also known as sensitivity, is TP / (TP + FN). It measures the ability to find all relevant instances. If 15 out of 20 real spam emails are detected, recall is 75%. This metric is critical when missing positives carries high risk, such as in cancer screening.

Image /page/11/Picture/0 description: The image shows a white balance scale against a light blue background. The scale is centered in the frame and takes up the majority of the space. The base of the scale is not visible, but the central pole extends upwards to a horizontal beam with a small ball on top. Two arms extend from the beam, each holding a shallow, round dish suspended by three thin chains. The dishes are empty and appear to be perfectly balanced. The light blue background is uniform and provides a clean, minimalist backdrop for the scale.

F1 Score: Balancing Precision and Recall

Precision: 83%

Accuracy of positive predictions.

Recall: 75%

Ability to identify all true positives.

F1 Score: ~78.8%

Harmonic mean of precision and recall.

The F1 Score is the harmonic mean of Precision and Recall: 2 × (Precision × Recall) / (Precision + Recall). With 83% precision and 75% recall, the F1 score is approximately 78.8%. This metric is particularly useful when dealing with imbalanced datasets, offering a balanced view of model performance.

Image /page/12/Picture/8 description: The image shows a graph with the words "False Positive Rate" written diagonally across the top right of the image. The y-axis is labeled "orRROCCF" vertically.

Specificity, ROC Curve, and AUC

![shield icon](https://i.imgur.com/919996l.png)

Specificity

TN / (TN + FP) measures true negatives.

Image /page/13/Picture/0 description: The image shows a line graph with a downward trend. The line starts at the top left, goes down, then up slightly, and then down again, ending with an arrow pointing downwards.

ROC Curve

Plots True Positive Rate vs. False Positive Rate.

Image /page/13/Picture/3 description: The image shows a blue line drawing of a graph. The graph has a horizontal base line, a vertical line on the left side, and a jagged line in the middle that resembles a mountain range.

AUC

Area Under the ROC Curve; higher AUC implies better model. It represents the probability that the classifier will rank a randomly chosen positive instance higher than a randomly chosen negative instance.

Specificity focuses on how well a model identifies true negatives. The ROC Curve visualizes classifier performance across all thresholds, plotting the True Positive Rate against the False Positive Rate. The Area Under the Curve (AUC) quantifies the overall performance of the classifier; a higher AUC indicates a better model.

Regression Metrics: MAE & RMSE

MAE (Mean Absolute Error)

Average of absolute errors. It's robust to outliers.

Image /page/14/Picture/0 description: The image shows a white, curved shape against a white background. The shape is roughly crescent-shaped, with a curved outer edge and a more complex inner edge that includes a curved section and a straight section. The shape appears to be a cutout or a design element, and the overall composition is simple and minimalist.

Image /page/14/Picture/1 description: The image shows a calculator icon. The calculator has a dark blue outline and a white fill. The calculator has a display screen at the top and a keypad with several buttons below. The buttons are arranged in a grid pattern.

RMSE (Root Mean Squared Error)

Square root of mean squared errors. Penalizes larger errors more severely.

Image /page/15/Picture/0 description: The image shows a white, curved shape on a white background. The shape is wider at the top and tapers towards the bottom. The shape has a curved inner edge and a curved outer edge. The shape is slightly angled to the left.

Use Cases

Ideal for continuous target variables, like predicting house prices.

Image /page/16/Picture/0 description: The image shows a white shape on a white background. The shape is curved and has a few sharp angles. In the bottom right corner of the image is a small icon of a person walking into a house.

For continuous target variables, such as house price prediction, Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) are key. MAE calculates the average of absolute errors, making it robust to outliers. RMSE, however, penalizes larger errors more, as it squares the errors before averaging.

Image /page/17/Picture/0 description: The image shows two puzzle pieces connected together. The puzzle pieces are light blue and white. The background is white.

Conclusion: Choosing the Right Metric

Context is Key

No single metric is universally best; it depends on the problem and business goals.

Holistic View

Combine multiple metrics for a complete understanding of model performance.

Align Goals

Ensure metric choice aligns with project objectives and class balance considerations.

The selection of the right metric is highly dependent on the specific problem and its business context. It's crucial to combine various metrics to gain a comprehensive understanding of model performance. Ultimately, your metric choice must align with your project goals and the balance of your dataset's classes.