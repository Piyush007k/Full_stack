import React, { useEffect, useState } from 'react';
import { Link,useLocation } from 'react-router-dom';

const Home = () => {
    const {state}=useLocation()
    console.log('Home');
    console.log(state);
  const [showButtons, setShowButtons] = useState(false);
  const [accessId, setAccessId] = useState('');
  const [Ranker, setRanker] = useState(false);
  const [Parser, setParser] = useState(false);
  const [Admin, setAdmin] = useState(false);

  useEffect(() => {
    if (state) {
        // Check if isAdmin is true1
        setAdmin(state.Is_admin === 'True1');
        
        // Check if Ranker and Parser are in app_access
        if (state.app_access.includes('Ranker')) {
            setRanker(true);
        }
        if (state.app_access.includes('Parser')) {
            setParser(true);
        }
    }
}, [state]);
return (
    <div>
        <div>
            <h3>Apps:</h3>
            <div>
                {Admin && (
                    <Link to="https://apps.powerapps.com/play/e/228140fb-0529-e4b8-b3ca-4d1613a7c5da/a/504422d8-9483-48d3-8a08-4aa1ccb39087?tenantId=b7182a97-d832-4b3a-ab2d-6848149387a3&hint=6dafd70b-a94a-4508-b21c-7cf3a1c5d3af&sourcetime=1711695855614">
                        <button>Power App</button>
                    </Link>
                )}
                {Ranker && (
                    <Link to="/ranker">
                        <button>Ranker</button>
                    </Link>
                )}
                {Parser && (
                    <Link to="/parser">
                        <button>Parser</button>
                    </Link>
                )}
            </div>
        </div>
    </div>
);
};

export default Home;
