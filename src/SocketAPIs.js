export const connect_to_doc = (socket, url, add_msg_cb, move_cursor_cb) => {
  socket.on('connect_to_doc', (data) => {
    console.log(data)
  })
  socket.on('add_msg', add_msg_cb)
  socket.on('move_cursor', move_cursor_cb)
  socket.emit('connect_to_doc', url)
}

export const add_msg = (socket, msg) => {
  console.log('RBZ sending msg: ', msg)
  socket.emit('add_msg', msg)
}

export const move_cursor = (socket, msg) => {
  socket.emit('move_cursor', msg)
}
