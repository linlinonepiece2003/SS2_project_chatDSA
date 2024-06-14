css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin-bottom: 1rem; 
    display: flex;
    overflow-wrap: break-word; /* Prevent long words from overflowing */
    word-wrap: break-word; /* Support for older browsers */
    word-break: break-word; /* Ensure words break as necessary */
    align-items: center; /* Center align items vertically */
}
.chat-message.user {
    background-color: #C6E2FF;
}
.chat-message.bot {
    background-color: #B9D3EE;
}
.chat-message .avatar {
    width: 20%;
}
.chat-message .avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #000000;
    overflow-wrap: break-word; /* Prevent long words from overflowing */
    word-wrap: break-word; /* Support for older browsers */
    word-break: break-word; /* Ensure words break as necessary */
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/BT2hmMR/images.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/V923xNt/anh-chibi-1-615x600.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''