import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState("");
  const [filteredData, setFilteredData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  // Fetch data from FastAPI
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/get-data")
      .then((response) => {
        setData(response.data);
        setFilteredData(response.data);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Handle Search
  const handleSearch = (event) => {
    setSearch(event.target.value);
    const filtered = data.filter((item) =>
      Object.values(item).some(
        (val) =>
          val &&
          val.toString().toLowerCase().includes(event.target.value.toLowerCase())
      )
    );
    setFilteredData(filtered);
    setCurrentPage(1);
  };

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredData.slice(indexOfFirstItem, indexOfLastItem);

  return (
    <div className="min-h-screen bg-gray-100 p-5">
      <h1 className="text-2xl font-bold mb-4 text-center">Excel-Like Table</h1>

      {/* Search Input */}
      <input
        type="text"
        placeholder="Search..."
        className="mb-4 p-2 border rounded w-full"
        value={search}
        onChange={handleSearch}
      />

      {/* Table */}
      <div className="overflow-auto">
        <table className="w-full border-collapse bg-white shadow-md rounded-lg">
          <thead>
            <tr className="bg-blue-500 text-white">
              <th className="p-2 border">ID</th>
              <th className="p-2 border">Địa Chỉ</th>
              <th className="p-2 border">Loại Dịch Vụ</th>
              <th className="p-2 border">Cước Tháng</th>
              <th className="p-2 border">ID Đầu Vào</th>
            </tr>
          </thead>
          <tbody>
            {currentItems.map((item, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="p-2 border text-center">{item.id}</td>
                <td className="p-2 border">{item.dia_chi}</td>
                <td className="p-2 border">{item.loai_dich_vu}</td>
                <td className="p-2 border text-right">{item.cuoc_thang}</td>
                <td className="p-2 border text-center">{item.id_dau_vao}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="mt-4 flex justify-center">
        {Array.from({ length: Math.ceil(filteredData.length / itemsPerPage) }, (_, i) => (
          <button
            key={i}
            className={`px-3 py-1 mx-1 rounded ${
              currentPage === i + 1 ? "bg-blue-500 text-white" : "bg-gray-300"
            }`}
            onClick={() => setCurrentPage(i + 1)}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default App;
