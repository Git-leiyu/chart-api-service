# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_file
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

app = Flask(__name__)

def create_er_diagram(entities_description):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    entities = []
    relationships = []
    
    lines = entities_description.split('\n')
    for line in lines:
        line = line.strip()
        if 'entity' in line.lower() or 'table' in line.lower():
            entities.append(line)
        elif 'relation' in line.lower() or 'relationship' in line.lower() or '->' in line:
            relationships.append(line)
    
    ax.clear()
    ax.set_title('Entity Relationship Diagram', fontsize=16, pad=20)
    
    # 使用英文标签
    entity_text = "Entities:\n" + "\n".join([f"• {e}" for e in entities]) if entities else "No entities defined"
    ax.text(0.1, 0.7, entity_text, fontsize=12, verticalalignment='top', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    relation_text = "Relationships:\n" + "\n".join([f"• {r}" for r in relationships]) if relationships else "No relationships defined"
    ax.text(0.1, 0.3, relation_text, fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    
    ax.text(0.5, 0.9, "Analysis Content:", fontsize=12, weight='bold', ha='center')
    ax.text(0.5, 0.85, entities_description[:100] + "..." if len(entities_description) > 100 else entities_description, 
            fontsize=10, ha='center', style='italic')
    
    ax.axis('off')
    plt.tight_layout()
    
    return fig

# 其余代码保持不变...
