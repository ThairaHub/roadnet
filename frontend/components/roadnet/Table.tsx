import React, { useState } from 'react';


type TableProps = {
  data: GroupedRoadFeature[];
  setRefresh: React.Dispatch<React.SetStateAction<boolean>>;
  selectedUpdatedAt: string | null;
  setSelectedUpdatedAt: (val: string) => void;
};

const Table: React.FC<TableProps> = ({ data, setRefresh, selectedUpdatedAt, setSelectedUpdatedAt }) => {


  const handleCheckboxChange = (updatedAt: string ) => {

      localStorage.setItem('selected_updated_at', updatedAt);
      setRefresh((prev: boolean) => !prev);
   
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-black border border-gray-200 rounded-lg">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Select</th>
            <th className="px-4 py-2 text-left">Updated At</th>
            <th className="px-4 py-2 text-left">Is Current</th>
            <th className="px-4 py-2 text-left">Customer ID</th>
            <th className="px-4 py-2 text-left">Geometry Points</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((row, index) => (
            <tr
              key={index}
              className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
            >
              <td className="px-4 py-2">
              {/* <input
                    type="checkbox"
                    onChange={(e) => {
                        if (e.target.checked) {
                        handleCheckboxChange(row.updated_at || "");
                        }
                    }}
                    /> */}
                    <input
                    type="radio"
                    name="selectedUpdatedAt"    // important: same name groups radios
                    value={row.updated_at || ""}
                    onChange={() => {

                        handleCheckboxChange(row.updated_at || "")
                        setSelectedUpdatedAt(row.updated_at || "");
                   
                    }}
                    />
              </td>
              <td className="px-4 py-2">
                {row.updated_at
                  ? new Date(row.updated_at).toLocaleString()
                  : '—'}
              </td>
              <td className="px-4 py-2">
                {row.is_current ? '✅ Yes' : '❌ No'}
              </td>
              <td className="px-4 py-2">{row.customer_id}</td>
              <td className="px-4 py-2">{row.geometry_points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
