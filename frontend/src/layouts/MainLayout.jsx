import { Outlet } from 'react-router-dom'
import AppShell from '../components/layout/AppShell'
import Sidebar from '../components/layout/Sidebar'
import Header from '../components/layout/Header'
import '../styles/layout.css'

function MainLayout() {
  return (
    <AppShell sidebar={<Sidebar />} header={<Header />}>
      <Outlet />
    </AppShell>
  )
}

export default MainLayout