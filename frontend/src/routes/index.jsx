import { createBrowserRouter } from 'react-router-dom'
import MainLayout from '../layouts/MainLayout'

function Placeholder({ title }) {
  return (
    <section>
      <h2>{title}</h2>
    </section>
  )
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        path: 'login',
        element: <Placeholder title="Login" />,
      },
      {
        path: 'dashboard',
        element: <Placeholder title="Dashboard" />,
      },
      {
        path: 'security',
        element: <Placeholder title="Security" />,
      },
      {
        path: 'security/monitor',
        element: <Placeholder title="Attack Monitor" />,
      },
      {
        path: 'security/events',
        element: <Placeholder title="Events" />,
      },
      {
        path: 'security/events/:eventId',
        element: <Placeholder title="Event Detail" />,
      },
      {
        path: 'security/search',
        element: <Placeholder title="Search" />,
      },
      {
        path: 'security/ip/:ip',
        element: <Placeholder title="IP Intelligence" />,
      },
      {
        path: 'response/policies',
        element: <Placeholder title="Policies" />,
      },
      {
        path: 'response/policies/new',
        element: <Placeholder title="New Policy" />,
      },
      {
        path: 'response/policies/:policyId',
        element: <Placeholder title="Policy Detail" />,
      },
      {
        path: 'response/history',
        element: <Placeholder title="Response History" />,
      },
      {
        path: 'response/history/:responseId',
        element: <Placeholder title="Response Detail" />,
      },
      {
        path: 'operations/audit',
        element: <Placeholder title="Audit Logs" />,
      },
      {
        path: 'operations/audit/:auditId',
        element: <Placeholder title="Audit Detail" />,
      },
      {
        path: 'operations/monitoring',
        element: <Placeholder title="Monitoring" />,
      },
      {
        path: 'operations/monitoring/:service',
        element: <Placeholder title="Service Monitoring" />,
      },
      {
        path: 'operations/backup',
        element: <Placeholder title="Backup Recovery" />,
      },
      {
        path: 'operations/reports',
        element: <Placeholder title="Reports" />,
      },
      {
        path: 'system/health',
        element: <Placeholder title="System Health" />,
      },
      {
        path: 'system/settings',
        element: <Placeholder title="Settings" />,
      },
      {
        path: 'system/settings/users',
        element: <Placeholder title="Users" />,
      },
      {
        path: 'system/settings/roles',
        element: <Placeholder title="Roles" />,
      },
      {
        path: 'system/settings/security',
        element: <Placeholder title="Security Settings" />,
      },
      {
        path: 'system/settings/notifications',
        element: <Placeholder title="Notification Settings" />,
      },
    ],
  },
])

export default router