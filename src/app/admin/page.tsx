'use client';

import React, { useState } from 'react';
import { AdminPortal } from '../../components/AdminPortal';
import '../../i18n/config';

export default function AdminPage() {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  return (
    <AdminPortal
      currentLanguage={currentLanguage}
    />
  );
} 