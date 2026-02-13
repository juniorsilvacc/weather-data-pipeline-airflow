from extract.extract_data import extract_weather_data

api_key = '747d68e78f13be9bc807ee19e4c18f84'
url = f'https://api.openweathermap.org/data/2.5/weather?q=Paraiba,BR&units=metric&appid={api_key}'

def main():
    print("Iniciando extração...")
    
    result = extract_weather_data(url)
    
    print("Extração finalizada.")
    print(result)

if __name__ == "__main__":
    main()
