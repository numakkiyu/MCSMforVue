export function isValidPort(port) {
  const num = parseInt(port)
  return !isNaN(num) && num >= 1 && num <= 65535
}

export function isValidHostname(hostname) {
  const pattern = /^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$/
  return pattern.test(hostname)
}

export function isValidIPv4(ip) {
  const pattern = /^(\d{1,3}\.){3}\d{1,3}$/
  if (!pattern.test(ip)) return false
  
  const parts = ip.split('.')
  return parts.every(part => {
    const num = parseInt(part)
    return num >= 0 && num <= 255
  })
}

export function isValidMinecraftAddress(address) {
  if (address.includes(':')) {
    const [host, port] = address.split(':')
    return (isValidHostname(host) || isValidIPv4(host)) && isValidPort(port)
  }
  return isValidHostname(address) || isValidIPv4(address)
} 