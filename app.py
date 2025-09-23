from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json
from calendar_sync import CalendarSync
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# グローバルなカレンダー同期インスタンス
calendar_sync = CalendarSync()

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/add_account', methods=['POST'])
def add_account():
    """新しいGoogleアカウントを追加"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'message': 'ユーザーIDが必要です'})
    
    if calendar_sync.add_user(user_id):
        return jsonify({'success': True, 'message': f'アカウント {user_id} が追加されました'})
    else:
        return jsonify({'success': False, 'message': 'アカウントの追加に失敗しました'})

@app.route('/remove_account', methods=['POST'])
def remove_account():
    """Googleアカウントを削除"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if calendar_sync.remove_user(user_id):
        return jsonify({'success': True, 'message': f'アカウント {user_id} が削除されました'})
    else:
        return jsonify({'success': False, 'message': 'アカウントの削除に失敗しました'})

@app.route('/get_events')
def get_events():
    """全アカウントのイベントを取得"""
    try:
        all_events = calendar_sync.get_all_events()
        return jsonify({'success': True, 'events': all_events})
    except Exception as e:
        return jsonify({'success': False, 'message': f'イベント取得エラー: {str(e)}'})

@app.route('/create_event', methods=['POST'])
def create_event():
    """新しいイベントを作成"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        event_data = {
            'summary': data.get('title'),
            'description': data.get('description', ''),
            'start': {
                'dateTime': data.get('start_time'),
                'timeZone': 'Asia/Tokyo'
            },
            'end': {
                'dateTime': data.get('end_time'),
                'timeZone': 'Asia/Tokyo'
            }
        }
        
        # 元のアカウントにイベントを作成
        if user_id not in calendar_sync.services:
            return jsonify({'success': False, 'message': '指定されたアカウントが見つかりません'})
        
        service = calendar_sync.services[user_id]
        created_event = service.create_event('primary', event_data)
        
        if created_event:
            # 他のアカウントに同期
            synced_events = calendar_sync.sync_event_to_all_accounts(user_id, event_data)
            
            return jsonify({
                'success': True, 
                'message': 'イベントが作成され、他のアカウントに同期されました',
                'original_event': created_event,
                'synced_events': synced_events
            })
        else:
            return jsonify({'success': False, 'message': 'イベントの作成に失敗しました'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'イベント作成エラー: {str(e)}'})

@app.route('/update_event', methods=['POST'])
def update_event():
    """既存のイベントを更新"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        event_id = data.get('event_id')
        event_data = {
            'summary': data.get('title'),
            'description': data.get('description', ''),
            'start': {
                'dateTime': data.get('start_time'),
                'timeZone': 'Asia/Tokyo'
            },
            'end': {
                'dateTime': data.get('end_time'),
                'timeZone': 'Asia/Tokyo'
            }
        }
        
        if user_id not in calendar_sync.services:
            return jsonify({'success': False, 'message': '指定されたアカウントが見つかりません'})
        
        service = calendar_sync.services[user_id]
        updated_event = service.update_event('primary', event_id, event_data)
        
        if updated_event:
            # 他のアカウントに同期
            synced_events = calendar_sync.sync_event_update_to_all_accounts(user_id, event_id, event_data)
            
            return jsonify({
                'success': True, 
                'message': 'イベントが更新され、他のアカウントに同期されました',
                'original_event': updated_event,
                'synced_events': synced_events
            })
        else:
            return jsonify({'success': False, 'message': 'イベントの更新に失敗しました'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'イベント更新エラー: {str(e)}'})

@app.route('/delete_event', methods=['POST'])
def delete_event():
    """イベントを削除"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        event_id = data.get('event_id')
        event_title = data.get('event_title')
        
        if user_id not in calendar_sync.services:
            return jsonify({'success': False, 'message': '指定されたアカウントが見つかりません'})
        
        service = calendar_sync.services[user_id]
        success = service.delete_event('primary', event_id)
        
        if success:
            # 他のアカウントからも削除
            deleted_events = calendar_sync.sync_event_deletion_to_all_accounts(user_id, event_id, event_title)
            
            return jsonify({
                'success': True, 
                'message': 'イベントが削除され、他のアカウントからも削除されました',
                'deleted_events': deleted_events
            })
        else:
            return jsonify({'success': False, 'message': 'イベントの削除に失敗しました'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'イベント削除エラー: {str(e)}'})

@app.route('/get_accounts')
def get_accounts():
    """登録されているアカウント一覧を取得"""
    accounts = list(calendar_sync.services.keys())
    return jsonify({'success': True, 'accounts': accounts})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
