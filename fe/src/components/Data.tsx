import { Box } from '@mui/material';
import { DataNode } from '../interfaces/TreeNode';
import BankData from './data/BankData';
import CityAccommodation from './data/CityAccommodation';
import CreditCardData from './data/CreditCardData';
import HelpItemData from './data/HelpItemData';
import GatheringData from './data/GatheringData';
import URLData from './data/URLData';
import SMSData from './data/SMSData';


export default function Data({ dataNode }: { dataNode: DataNode }) {
  const renderData = () => {
    if (dataNode.data.dataType === 'city-accommodation') {
      return <CityAccommodation value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'bank-account-donation') {
      return <BankData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'credit-card-donation') {
      return <CreditCardData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'international-bank-account-donation') {
      return <BankData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'international-url-donation') {
      return <URLData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'gathering-list') {
      return <GatheringData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'help-item-list') {
      return <HelpItemData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'url-donation') {
      return <URLData value={dataNode.data as any} />
    }

    if (dataNode.data.dataType === 'sms-donation') {
      return <SMSData value={dataNode.data as any} />
    }

    return <></>;
  };

  return (
    <Box>
      <Box sx={{ textAlign: 'center', display: 'flex', flexFlow: 'column nowrap', justifyContent: 'center', alignItems: 'center' }}>
        {renderData()}
      </Box>
    </Box>
  );
};
