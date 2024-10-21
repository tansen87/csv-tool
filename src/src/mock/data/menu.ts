const menus: any[] = [
  {
    name: 'home page',
    icon: 'yibiaopan2',
    path: '/',
  },
  // {
  //   path: '/icon',
  //   icon: 'tubiao',
  //   name: '图标',
  // },
  // {
  //   path: '/datetime',
  //   icon: 'riqishijian',
  //   name: '日期时间',
  // },
  // {
  //   path: '/table',
  //   icon: 'biaoge',
  //   name: '配置化表格',
  // },
]

export default [
  {
    url: '/api/menus',
    data: () => menus,
  },
]
