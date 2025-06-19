require('dotenv').config();
const express = require('express');
const http = require('http');
const cors = require('cors');
const { Server } = require('socket.io');

const app = express();
app.use(cors());

const server = http.createServer(app);

const io = new Server(server, {
    cors: {
        origin: process.env.FRONTEND_URL || "http://localhost:3000",
        methods: ["GET", "POST"],   
    },
});

io.on('connection', (socket) => {
    console.log(`User connected: ${socket.id}`);
    
    socket.on('join_chat', (chatroomId) => {
        socket.join(chatroomId);
        console.log(`User ${socket.id} joined chat: ${chatroomId}`);
    });

    socket.on('send_message', (data) => {
        console.log('Message received:', data);
        io.emit('receive_message', data);
        
        io.emit('chatlist_update', {
            chat_id: data.room,
            last_message: data
        });
    });

    socket.on('messages_read', (data) => {
        console.log('Messages marked as read:', data);
        io.emit('message_status_updated', data);
    });

    socket.on('disconnect', () => {
        console.log(`User disconnected: ${socket.id}`);
    });
});
const PORT = process.env.WEBSOCKET_PORT || 4000;
server.listen(PORT, () => {
    console.log(`WebSocket server is running on port ${PORT}`);
});