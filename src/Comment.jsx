import React, { useState } from 'react'
import './Comment.css'
import { getUserColour } from './Constants.js'
import Form from 'react-bootstrap/Form'

function Message(props) {
  const userColor = getUserColour(props.data.user)
  return (
    <div className="message">
      <div className="messageAuthor" style={{ color: userColor }}>
        {props.data.user}
      </div>
      <div className="messageBody"> {props.data.body}</div>
    </div>
  )
}

function ReplyForm(props) {
  const [replyMessage, setReplyMessage] = useState('');

  const handleCommentTextChange = (e) => {
    setReplyMessage(e.target.value);
  }
  const handleKeyPress = (target) => {
    if (target.charCode == 13) {
      setReplyMessage('');
      props.addNewMessage({
        message_thread_id: props.messageThreadId,
        body: replyMessage,
      });
    }
  }

  return (
    <Form.Group controlId="formReply">
      <Form.Control
        type="text"
        placeholder="Reply"
        value={replyMessage}
        onChange={handleCommentTextChange}
        onKeyPress={handleKeyPress}
        className="reply"
      />
    </Form.Group>
  )
}

export default function CommentThread(props) {
  const [messageThreadData] = useState(
    props.messageThreadData,
  )
  const borderColor = getUserColour(messageThreadData.messages[0].user)
  return (
    <div
      className="messageThread"
      style={{
        left: messageThreadData.left + 'px',
        top: messageThreadData.top + 'px',
        position: 'absolute',
        borderColor: borderColor,
      }}
    >
      {messageThreadData.messages.map((messageData) => (
        <Message data={messageData} />
      ))}
      <ReplyForm
        messageThreadId={messageThreadData.message_thread_id}
        addNewMessage={props.addNewMessage}
      />
    </div>
  )
}
