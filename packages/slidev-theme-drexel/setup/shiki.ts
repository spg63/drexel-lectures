import { defineShikiSetup } from '@slidev/types'

// Light code on the paper ground; vitesse is low-saturation enough not to fight the palette.
export default defineShikiSetup(() => ({
  themes: { light: 'vitesse-light', dark: 'vitesse-light' },
}))
