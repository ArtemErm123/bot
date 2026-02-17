import React from 'react'
import ReactDOM from 'react-dom/client'
import { CssBaseline, Container, Typography } from '@mui/material'

const App = () => (
  <>
    <CssBaseline />
    <Container>
      <Typography variant="h4" mt={4}>
        Bot Frontend Scaffold
      </Typography>
    </Container>
  </>
)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
