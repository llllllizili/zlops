export const getWebSocket = () => {
    let protocol = document.location.protocol === 'https:' ? 'wss://' : 'ws://'
    let url = protocol + document.location.host + '/nms/ws/'
    let ws = new WebSocket(url)
    ws.onopen = onOpen
    ws.onclose = onClose
    return ws
  }