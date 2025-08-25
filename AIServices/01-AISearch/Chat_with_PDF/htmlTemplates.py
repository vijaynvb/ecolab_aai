css = '''
<style>
body {
    background: #23272f;
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 0;
}
.chat-container {
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    background: #262b36;
    border-radius: 1rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.2);
}
.chat-message {
    padding: 1.2rem 1.5rem;
    border-radius: 1.2rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: flex-end;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    position: relative;
}
.chat-message.user {
    background-color: #2b313e;
    flex-direction: row-reverse;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 56px;
    min-width: 56px;
    margin: 0 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
}
.chat-message .avatar img {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #fff2;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.chat-message .message {
    width: auto;
    max-width: 80%;
    padding: 0.8rem 1.2rem;
    color: #fff;
    background: rgba(0,0,0,0.08);
    border-radius: 1rem;
    position: relative;
    font-size: 1.08rem;
    line-height: 1.5;
}
.chat-message.user .message {
    background: #36405a;
}
.chat-message.bot .message {
    background: #3a4254;
}
.chat-message.user .message:after {
    content: '';
    position: absolute;
    right: -12px;
    top: 18px;
    border-width: 8px 0 8px 12px;
    border-style: solid;
    border-color: transparent transparent transparent #36405a;
}
.chat-message.bot .message:after {
    content: '';
    position: absolute;
    left: -12px;
    top: 18px;
    border-width: 8px 12px 8px 0;
    border-style: solid;
    border-color: transparent #3a4254 transparent transparent;
}
.timestamp {
    font-size: 0.85rem;
    color: #b0b6c3;
    margin-top: 0.2rem;
    margin-left: 1.2rem;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar" style="font-size: 2.5rem; display: flex; align-items: center; justify-content: center;">🤖</div>
    <div>
        <div class="message">{{MSG}}</div>
        <div class="timestamp">{{TIME}}</div>
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar" style="font-size: 2.5rem; display: flex; align-items: center; justify-content: center;">🧑</div>
    <div>
        <div class="message">{{MSG}}</div>
        <div class="timestamp">{{TIME}}</div>
    </div>
</div>
'''
