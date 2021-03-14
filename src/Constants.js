export const USER_BLUE = '#00BFF3'
export const USER_GREEN = '#00FF00'
export const USER_ORANGE = '#FC6A03'
export const USER_VIOLET = '#8A2BE2'
export const USER_RED = '#DC143D'

export const getUserColour = (user) => {
  switch (user) {
    case 'Pratyay':
      return USER_BLUE
    case 'Debdut':
      return USER_GREEN
    case 'Sandipan':
      return USER_VIOLET
      case 'Saif':
        return USER_ORANGE
    default:
      return USER_RED
  }
}
