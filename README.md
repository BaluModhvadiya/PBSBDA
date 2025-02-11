# PBSBDA
Prompt based search in big data analytics

# PBSBDA - Big Data Analytics Query Dashboard

PBSBDA (Prompt-Based Search for Big Data Analytics) is an end-to-end application for querying and visualizing big data insights through natural language inputs. It combines a backend powered by Apache Spark and FastAPI with a modern React-based frontend using TailwindCSS.

---

## **Features**

- **Natural Language Querying**: Converts natural language inputs into SQL queries using an integrated AI model.
- **Big Data Processing**: Leverages Apache Spark for efficient query execution on large datasets.
- **Interactive Dashboard**: Provides real-time results and visualizations through a responsive frontend.
- **Scalability**: Supports HDFS and other big data storage solutions.

---

## **Project Structure**

```plaintext
PBSBDA/
├── backend/
│   ├── app.py               # Backend API powered by FastAPI
│   ├── cleanup_spark.sh     # Script for Spark environment cleanup
│   ├── ecommerce_data/      # Sample big data for testing
│   ├── Final_Merged_Dataset.csv  # Dataset (ignored in `.gitignore`)
│   ├── metastore_db/        # Spark metastore
│   ├── process_reviews.py   # Script to preprocess review data
│   ├── spark-warehouse/     # Spark output directory
├── docs/                    # Documentation (currently empty)
├── frontend/
│   ├── src/                 # React application source code
│   │   ├── App.jsx          # Main dashboard component
│   │   ├── App.css          # TailwindCSS for styling
│   │   ├── assets/          # Static assets (images, icons, etc.)
│   │   ├── main.jsx         # Entry point for React
│   ├── index.html           # HTML entry file for Vite
│   ├── package.json         # Frontend dependencies
│   ├── tailwind.config.cjs  # TailwindCSS configuration
│   ├── vite.config.js       # Vite configuration
├── tests/                   # Unit and integration tests (currently empty)
├── README.md                # Project documentation
└── .gitignore               # Files and directories to ignore in version control
```

---

## **Getting Started**

### Prerequisites

- **Backend**:
  - Python 3.8 or later
  - Apache Spark 3.4.4
  - FastAPI
- **Frontend**:
  - Node.js 16 or later
  - React 18+
  - TailwindCSS 2.2.19
- **Big Data Storage**:
  - HDFS (Hadoop Distributed File System)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/PBSBDA.git
   cd PBSBDA
   ```

2. **Backend Setup**:
   - Navigate to `backend/`:
     ```bash
     cd backend
     ```
   - Create a virtual environment:
     ```bash
     python3 -m venv myenv
     source myenv/bin/activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the FastAPI server:
     ```bash
     uvicorn app:app --reload
     ```

3. **Frontend Setup**:
   - Navigate to `frontend/`:
     ```bash
     cd frontend
     ```
   - Install Node.js dependencies:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm run dev
     ```

4. Access the application at:
   ```
   http://localhost:5173
   ```

---

## **Usage**

- Enter natural language queries in the dashboard.
- View generated SQL, latency metrics, and visualized results.
- Modify and preprocess datasets in the `backend/ecommerce_data` directory.

---

## **Contributing**

Contributions are welcome! Please follow the steps in the `CONTRIBUTING.md` file (coming soon).

---

## **License**

This project is licensed under the MIT License.

---

## **Acknowledgments**

Special thanks to open-source communities behind Apache Spark, React, FastAPI, and TailwindCSS.


