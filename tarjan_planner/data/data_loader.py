import csv
import re
from typing import List, Dict
import os
import logging

class RelativesDataLoader:
    def __init__(self, file_path='relatives_data.csv'):
        self.file_path = file_path
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_relatives(self) -> List[Dict]:
        """
        Load relatives data from CSV, validate using regex
        
        Returns:
            List of dictionaries containing relative information
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Data file not found: {self.file_path}")
        
        relatives = []
        try:
            with open(self.file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned_row = self._clean_and_validate_row(row)
                    if cleaned_row:
                        relatives.append(cleaned_row)
        except csv.Error as e:
            self.logger.error(f"Error reading CSV file: {e}")
            raise ValueError(f"Error reading CSV file: {e}")
        
        if not relatives:
            raise ValueError("No valid relative data found in the file")
        
        self.logger.info(f"Loaded {len(relatives)} relatives successfully.")
        return relatives
    
    def _clean_and_validate_row(self, row: Dict) -> Dict:
        """
        Clean and validate a single row of relative data
        
        Args:
            row (Dict): Raw data row from CSV
        
        Returns:
            Dict: Validated and cleaned row, or None if invalid
        """
        lat_pattern = r'^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$'
        lon_pattern = r'^-?(1[0-7]\d|[1-9]?\d)(\.\d+)?$'
        
        try:
            lat = row.get('latitude', '').strip()
            lon = row.get('longitude', '').strip()
            
            if not re.match(lat_pattern, lat) or not re.match(lon_pattern, lon):
                self.logger.warning(f"Invalid coordinates for {row.get('relative', 'Unknown')}")
                return None
            
            required_fields = ['relative', 'street_name', 'district', 'latitude', 'longitude']
            if not all(row.get(field) for field in required_fields):
                self.logger.warning(f"Missing fields in row: {row}")
                return None
            
            return {
                'relative': row['relative'],
                'street_name': row['street_name'],
                'district': row['district'],
                'latitude': float(lat),
                'longitude': float(lon)
            }
        except Exception as e:
            self.logger.error(f"Error processing row: {e}")
            return None
    
    def create_sample_data(self):
        """
        Create a sample CSV file if it doesn't exist
        """
        if not os.path.exists(self.file_path):
            sample_data = [
                ['relative', 'street_name', 'district', 'latitude', 'longitude'],
                ['Relative_1', 'Gangnam-daero', 'Gangnam-gu', '37.4979', '127.0276'],
                ['Relative_2', 'Yangjae-daero', 'Seocho-gu', '37.4833', '127.0322'],
                ['Relative_3', 'Sinsa-daero', 'Gangnam-gu', '37.5172', '127.0286'],
                ['Relative_4', 'Apgujeong-ro', 'Gangnam-gu', '37.5219', '127.0411'],
                ['Relative_5', 'Hannam-daero', 'Yongsan-gu', '37.5340', '127.0026'],
                ['Relative_6', 'Seongsu-daero', 'Seongdong-gu', '37.5443', '127.0557'],
                ['Relative_7', 'Cheongdam-ro', 'Gangnam-gu', '37.5172', '127.0391'],
                ['Relative_8', 'Bukhan-ro', 'Jongno-gu', '37.5800', '126.9844'],
                ['Relative_9', 'Samseong-ro', 'Gangnam-gu', '37.5110', '127.0590'],
                ['Relative_10', 'Jamsil-ro', 'Songpa-gu', '37.5133', '127.1028'],
            ]
            
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(sample_data)