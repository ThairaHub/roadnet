'use client'

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import Cookies from 'js-cookie';
import Table from "./Table";
import { geoJsonApi } from "@/lib/api/geojson";


const Map = dynamic(async () => await import("@/components/Map"), { ssr: false }); 


export default function RoadNetPage() {
  const [geojson, setGeojson] = useState(null);
  const [tableData, setTableData] = useState<GroupedRoadFeature[]>([])
  const [refresh, setRefresh] = useState(false);
  const [selectedUpdatedAt, setSelectedUpdatedAt] = useState<string | null>(null);


  useEffect(() => {
    const fetchTableData = async () => {

      const res = await geoJsonApi.get_roadstimestamp()

      setTableData(res.data);
    };
    fetchTableData();
    console.log("refresh", refresh)
  }, []);


  useEffect(() => {
    const fetchData = async () => {
      const filterData = localStorage.getItem("selected_updated_at") || ""
    
      let endpoint = "roads"
      if (filterData){
        endpoint = `roads?as_of=${filterData}`
      }
      
      const res = await geoJsonApi.get_roads_with_date(endpoint)
      if(res.data) {
        setGeojson(res.data);
      }

    };
  
    fetchData();
  }, [refresh]); // runs every time refresh changes


  console.log(geojson)


  return (
    <main className="flex flex-col h-screen w-screen">

    <Table 
      data={tableData} setRefresh={setRefresh}
      selectedUpdatedAt={selectedUpdatedAt}
      setSelectedUpdatedAt={setSelectedUpdatedAt}
      />
    <br/>
        {/* <FileUpload /> */}
        {/* <Sidebar /> */}
        <Map geojson={geojson} />

    </main>
  );
}
