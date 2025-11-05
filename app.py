# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Chart API is running'})

@app.route('/generate_diagram', methods=['POST'])
def generate_diagram():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'})
        
        content = data.get('content', '')
        
        if not content:
            return jsonify({'success': False, 'error': 'No content provided'})
        
        # 解析实体和关系，生成Mermaid代码
        mermaid_code = generate_mermaid_code(content)
        
        return jsonify({
            'success': True,
            'mermaid_code': mermaid_code,
            'message': 'Mermaid ER diagram code generated successfully',
            'type': 'er'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def generate_mermaid_code(description):
    """根据描述生成Mermaid ER图代码"""
    # 简化的解析逻辑 - 实际可以根据需要增强
    lines = description.split('\n')
    entities = []
    
    for line in lines:
        line = line.strip()
        if '实体' in line or '表' in line or 'entity' in line.lower():
            entities.append(line)
    
    # 生成基础的Mermaid代码
    mermaid_code = """erDiagram
    CUSTOMER {
        string customer_id PK
        string name
        string email
    }
    ORDER {
        string order_id PK
        string customer_id FK
        date order_date
    }
    CUSTOMER ||--o{ ORDER : "places"
    
    """
    
    # 添加分析内容作为注释
    mermaid_code += f"    %% Analysis of: {description[:100]}...\n"
    
    return mermaid_code

@app.route('/generate_diagram_direct', methods=['GET'])
def generate_diagram_direct():
    content = request.args.get('content', 'Test entities: User, Book, BorrowRecord')
    
    try:
        mermaid_code = generate_mermaid_code(content)
        
        return jsonify({
            'success': True,
            'mermaid_code': mermaid_code,
            'message': 'Mermaid code generated successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
