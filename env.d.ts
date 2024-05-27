/// <reference types="vite/client" />
declare module '*.js'
declare module '*.mjs'

declare module 'vuex' {
    const content: any
    export = content
  }