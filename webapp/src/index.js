import { createRoot } from 'react-dom/client'
import './App.css'
import App from './App'
import { Leva } from 'leva'
import React from 'react'


createRoot(document.getElementById('root')).render(
  <>
    <App />
    
    <Leva  />
  </>
)
