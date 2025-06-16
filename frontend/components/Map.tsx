'use client';

import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";
import L from "leaflet";
import StreetModal from "./StreetModal";

type MapProps = {
  geojson: GeoJSON.FeatureCollection | null;
};

function FitBoundsOnGeoJSON({ data }: { data: GeoJSON.GeoJsonObject }) {
    const map = useMap();

    console.log("data", data)
    useEffect(() => {
      if (!data) return;
  
      const geoJsonLayer = L.geoJSON(data);
      const bounds = geoJsonLayer.getBounds();
  
      if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [50, 50] });
      } 
    }, [data, map]);
  
    return null;
  }



export default function Map({ geojson }: MapProps) {
const [selectedStreet, setSelectedStreet] = useState<any>(null);
const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    // Fix leaflet marker icon path issues
    delete (L.Icon.Default.prototype as any)._getIconUrl;

    L.Icon.Default.mergeOptions({
      iconRetinaUrl:
        "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png",
      iconUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png",
      shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
    });
  }, []);

  const onEachFeature = (feature: any, layer: any) => {
    layer.on("click", () => {
      setSelectedStreet(feature.properties);
      setIsModalOpen(true);
    });
  };

  return (
    <div className="flex-1 relative">
                <StreetModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        street={selectedStreet}
      />
        <MapContainer
        center={[0,0]}
        zoom={13}
        scrollWheelZoom={true}
        className="h-full w-full z-0 relative"
        >
        <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {geojson && (
                    <>
                    <GeoJSON 
                            key={JSON.stringify(geojson)} // ⚠️ change this key when data changes
                            data={geojson} 
                            style={{ color: "#333", weight: 5 }} 
                            onEachFeature={onEachFeature} />

                    <FitBoundsOnGeoJSON data={geojson} />
                </>
        )}

        
        </MapContainer>


        {/* <div className="absolute top-4 left-4 bg-white p-2 shadow rounded">
            <input
            type="text"
            className="border p-1 text-sm"
            placeholder="Heisingen Test"
            />
        </div> */}
    </div>
  );
}
