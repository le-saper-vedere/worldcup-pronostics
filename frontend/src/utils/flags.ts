const FIFA_TO_ISO: Record<string, string> = {
  // Group A
  MEX: 'MX',
  RSA: 'ZA',
  KOR: 'KR',
  CZE: 'CZ',
  // Group B
  CAN: 'CA',
  BIH: 'BA',
  QAT: 'QA',
  SUI: 'CH',
  // Group C
  BRA: 'BR',
  MAR: 'MA',
  HAI: 'HT',
  SCO: 'GB-SCT',
  // Group D
  USA: 'US',
  PAR: 'PY',
  AUS: 'AU',
  TUR: 'TR',
  // Group E
  GER: 'DE',
  CUW: 'CW',
  CIV: 'CI',
  ECU: 'EC',
  // Group F
  NED: 'NL',
  JPN: 'JP',
  SWE: 'SE',
  TUN: 'TN',
  // Group G
  BEL: 'BE',
  EGY: 'EG',
  IRN: 'IR',
  NZL: 'NZ',
  // Group H
  ESP: 'ES',
  CPV: 'CV',
  KSA: 'SA',
  URU: 'UY',
  // Group I
  FRA: 'FR',
  SEN: 'SN',
  IRQ: 'IQ',
  NOR: 'NO',
  // Group J
  ARG: 'AR',
  ALG: 'DZ',
  AUT: 'AT',
  JOR: 'JO',
  // Group K
  POR: 'PT',
  COD: 'CD',
  UZB: 'UZ',
  COL: 'CO',
  // Group L
  ENG: 'GB-ENG',
  CRO: 'HR',
  GHA: 'GH',
  PAN: 'PA',
}

export const flagUrl = (fifaCode: string): string | null => {
  const iso = FIFA_TO_ISO[fifaCode]
  return iso ? `https://flagcdn.com/${iso.toLowerCase()}.svg` : null
}
