from get_data import get_data
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.multiclass import OneVsRestClassifier
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image as XLImage
from openpyxl.chart import BarChart, Reference
import joblib
import json
import os
import numpy as np
from openpyxl.styles import Alignment

data = get_data()
X = []
y = []
for item in data:
    X.extend(item["texts"])
    y.extend([item["intent"]] * len(item["texts"]))

# Vectorizador general
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# Función para graficar y guardar imágenes
def plot_and_save_graphs(df_report, sheet_name):
    fig, ax = plt.subplots(figsize=(8, 4))
    df = df_report[df_report['class'].isin(['accuracy', 'macro avg', 'weighted avg']) == False]
    df[['precision', 'recall', 'f1-score']].plot(kind='bar', ax=ax, title=f"{sheet_name} - Métricas por clase", legend=True)
    ax.set_xticks(range(len(df['class'])))
    ax.set_xticklabels(df['class'], rotation=45, ha='right')
    plt.tight_layout()
    bar_path = f"./tmp/{sheet_name}_bar.png"
    plt.savefig(bar_path)
    plt.close()

    # Pastel de soporte por clase
    fig, ax = plt.subplots()
    df.plot.pie(y='support', labels=df['class'], ax=ax, autopct='%1.1f%%', legend=False)
    ax.set_ylabel('')
    ax.set_title(f"{sheet_name} - Distribución de soporte")
    pie_path = f"./tmp/{sheet_name}_pie.png"
    plt.tight_layout()
    plt.savefig(pie_path)
    plt.close()
    return bar_path, pie_path

# Crear nuevo archivo con gráficas añadidas
wb = Workbook()
wb.remove(wb.active)

for test_size in [0.1, 0.2, 0.3, 0.4]:
    sheet_name = f"test_size_{int(test_size*100)}"
    ws = wb.create_sheet(sheet_name)

    # Split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, stratify=y, random_state=42)
    X_train_tfidf = vectorizer.transform(X_train)
    X_val_tfidf = vectorizer.transform(X_val)

    # Modelo
    model = OneVsRestClassifier(LogisticRegression())
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_val_tfidf)

    # Reporte
    report = classification_report(y_val, y_pred, output_dict=True)
    df_report = pd.DataFrame(report).transpose().reset_index().rename(columns={"index": "class"})
    for r in dataframe_to_rows(df_report, index=False, header=True):
        ws.append(r)

    # Insertar gráficas
    bar_img, pie_img = plot_and_save_graphs(df_report, sheet_name)
    img_bar = XLImage(bar_img)
    img_pie = XLImage(pie_img)
    ws.add_image(img_bar, "J2")
    ws.add_image(img_pie, "J25")

    # Matriz de Confusión
    cm = confusion_matrix(y_val, y_pred)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.matshow(cm, cmap='Blues')
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, f'{val}', ha='center', va='center', color='red')
    ax.set_title(f"{sheet_name} - Matriz de Confusión")
    ax.set_xlabel('Predicción')
    ax.set_ylabel('Realidad')
    plt.tight_layout()
    cm_img_path = f"./tmp/{sheet_name}_cm.png"
    plt.savefig(cm_img_path)
    plt.close()

    # Insertar la imagen de la matriz de confusión
    img_cm = XLImage(cm_img_path)
    ws.add_image(img_cm, "A25")

    # Validación cruzada 5-fold
    cross_val_scores = cross_val_score(model, X_train_tfidf, y_train, cv=5, scoring='accuracy')
    avg_cross_val_score = cross_val_scores.mean()

    # Insertar resultado de validación cruzada
    ws.append([])
    ws.append(["Validación cruzada 5-fold (solo en entrenamiento)"])
    ws.append(['Scores por fold', *cross_val_scores])
    ws.append([f'Promedio de accuracy', f"{avg_cross_val_score:.4f}"])

# Guardar nuevo archivo
excel_with_graphs = "./tmp/metrics_IA_K8S.xlsx"
wb.save(excel_with_graphs)
excel_with_graphs
