CREATE OR REPLACE FUNCTION public.add_break_history(add_break character varying, add_error_code character varying)
 RETURNS void
 LANGUAGE sql
AS $function$
	INSERT INTO break_history (break, error_code) VALUES (add_break, add_error_code);
$function$
;

CREATE OR REPLACE FUNCTION public.add_car(add_car_brand character varying, add_vin character varying, add_car_color character varying, add_car_model character varying, add_release_year date, add_engine_type character varying, add_fuel_type character varying, add_engine_capacity character varying, add_transmission_type character varying, add_user_id integer)
 RETURNS void
 LANGUAGE sql
AS $function$
	INSERT INTO car (car_brand, vin_code, car_color, car_model, release_year, engine_type, fuel_type, engine_capacity, transmission_type, user_id) VALUES (add_car_brand, add_vin, add_car_color, add_car_model, add_release_year, add_engine_type, add_fuel_type, add_engine_capacity, add_transmission_type, add_user_id);
$function$
;

CREATE OR REPLACE FUNCTION public.create_match(p_map_id integer, p_team1_id integer, p_team2_id integer, p_match_date date, p_match_status character varying)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
DECLARE
    v_match_id INT;
BEGIN
    INSERT INTO Matches (map_id, team1_id, team2_id, match_date, match_status)
    VALUES (p_map_id, p_team1_id, p_team2_id, p_match_date, p_match_status)
    RETURNING match_id INTO v_match_id;
    
    RETURN v_match_id;
EXCEPTION
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Ошибка внешнего ключа (карта или команда не существует)';
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Ошибка при создании матча: %', SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.add_servis_history(add_car_id integer, add_motor_oil character varying DEFAULT NULL::character varying, add_air_filter character varying DEFAULT NULL::character varying, add_transmission_oil character varying DEFAULT NULL::character varying, add_cabin_filter character varying DEFAULT NULL::character varying, add_oil_filter character varying DEFAULT NULL::character varying, add_fuel_filter character varying DEFAULT NULL::character varying, add_mileage character varying DEFAULT NULL::character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    INSERT INTO service_history (
        car_id,
        motor_oil,
        air_filter,
        transmission_oil,
        cabin_filter,
        oil_filter,
        fuel_filter,
        mileage
    ) VALUES (
        add_car_id,
        add_motor_oil,
        add_air_filter,
        add_transmission_oil,
        add_cabin_filter,
        add_oil_filter,
        add_fuel_filter,
        add_mileage
    );
END;
$function$
;

CREATE OR REPLACE FUNCTION public.delete_break_history(p_car_id integer)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    
    DELETE FROM public.break_history WHERE car_id = p_car_id;
    
    RETURN 'Данные о поломках успешно удалены';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при удалении: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.delete_car(p_car_id integer)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    DELETE FROM public.garage WHERE car_id = p_car_id;
    DELETE FROM public.service_history WHERE car_id = p_car_id;
    DELETE FROM public.break_history WHERE car_id = p_car_id;
    
    DELETE FROM public.car WHERE car_id = p_car_id;
    
    RETURN 'Автомобиль и все связанные записи успешно удалены';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при каскадном удалении: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.delete_garage(p_car_id integer)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    
    DELETE FROM public.garage WHERE car_id = p_car_id;
    
    RETURN 'Данные о машине успешно удалены';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при удалении: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.delete_service_history(p_car_id integer)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    
    DELETE FROM public.service_history WHERE car_id = p_car_id;
    
    RETURN 'Данные о заменах успешно удалены';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при удалении: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_break_history(p_old_car_id integer, p_new_car_id integer DEFAULT NULL::integer, p_break character varying DEFAULT NULL::character varying, p_error_code character varying DEFAULT NULL::character varying)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    update_count INT;
    v_car_exists BOOLEAN;
BEGIN
    -- 1. Проверяем существование исходной записи
    IF NOT EXISTS (SELECT 1 FROM public.break_history WHERE car_id = p_old_car_id) THEN
        RETURN 'Ошибка: запись с car_id ' || p_old_car_id || ' не найдена';
    END IF;
    
    -- 2. Если указан новый car_id, выполняем проверки
    IF p_new_car_id IS NOT NULL AND p_new_car_id != p_old_car_id THEN
        -- Проверяем существование нового автомобиля
        SELECT EXISTS (SELECT 1 FROM public.car WHERE car_id = p_new_car_id) 
        INTO v_car_exists;
        
        IF NOT v_car_exists THEN
            RETURN 'Ошибка: автомобиль с ID ' || p_new_car_id || ' не существует';
        END IF;
        
        -- Проверяем уникальность нового car_id в break_history
        IF EXISTS (SELECT 1 FROM public.break_history WHERE car_id = p_new_car_id) THEN
            RETURN 'Ошибка: запись с car_id ' || p_new_car_id || ' уже существует';
        END IF;
    END IF;
    
    -- 3. Выполняем обновление
    UPDATE public.break_history
    SET 
        car_id = COALESCE(p_new_car_id, car_id),
        break = COALESCE(p_break, break),
        error_code = COALESCE(p_error_code, error_code)
    WHERE car_id = p_old_car_id;
    
    -- 4. Проверяем результат
    GET DIAGNOSTICS update_count = ROW_COUNT;
    
    IF update_count > 0 THEN
        RETURN 'Данные успешно обновлены. ' ||
               CASE WHEN p_new_car_id IS NOT NULL THEN 
                    'Новый car_id: ' || p_new_car_id 
               ELSE 'car_id не изменен' END;
    ELSE
        RETURN 'Нет изменений для car_id ' || p_old_car_id;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при обновлении: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_car(p_car_id integer, p_car_brand character varying DEFAULT NULL::character varying, p_vin_code character varying DEFAULT NULL::character varying, p_car_color character varying DEFAULT NULL::character varying, p_car_model character varying DEFAULT NULL::character varying, p_release_year integer DEFAULT NULL::integer, p_engine_type character varying DEFAULT NULL::character varying, p_fuel_type character varying DEFAULT NULL::character varying, p_engine_capacity character varying DEFAULT NULL::character varying, p_transmission_type character varying DEFAULT NULL::character varying)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    current_record RECORD;
    update_query TEXT;
    updates TEXT[] := '{}';
    result_message TEXT;
BEGIN
    -- Проверяем существование автомобиля
    SELECT * INTO current_record FROM public.car WHERE car_id = p_car_id;
    IF NOT FOUND THEN
        RETURN 'Ошибка: автомобиль с ID ' || p_car_id || ' не найден';
    END IF;
    
    -- Проверяем VIN код на уникальность (если он был передан)
    IF p_vin_code IS NOT NULL AND p_vin_code != current_record.vin_code THEN
        IF EXISTS (SELECT 1 FROM public.car WHERE vin_code = p_vin_code AND car_id != p_car_id) THEN
            RETURN 'Ошибка: VIN код ' || p_vin_code || ' уже существует в системе';
        END IF;
        
        -- Проверяем длину VIN кода (стандарт - 17 символов)
        IF LENGTH(p_vin_code) != 17 THEN
            RETURN 'Ошибка: VIN код должен содержать ровно 17 символов';
        END IF;
        
        updates := updates || format('vin_code = %L', p_vin_code);
    END IF;
    
    -- Формируем части запроса для других полей
    IF p_car_brand IS NOT NULL AND p_car_brand != current_record.car_brand THEN
        updates := updates || format('car_brand = %L', p_car_brand);
    END IF;
    
    IF p_car_color IS NOT NULL AND p_car_color != current_record.car_color THEN
        updates := updates || format('car_color = %L', p_car_color);
    END IF;
    
    IF p_car_model IS NOT NULL AND p_car_model != current_record.car_model THEN
        updates := updates || format('car_model = %L', p_car_model);
    END IF;
    
    IF p_release_year IS NOT NULL AND p_release_year != current_record.release_year THEN
        updates := updates || format('release_year = %L', p_release_year);
    END IF;
    
    IF p_engine_type IS NOT NULL AND p_engine_type != current_record.engine_type THEN
        updates := updates || format('engine_type = %L', p_engine_type);
    END IF;
    
    IF p_fuel_type IS NOT NULL AND p_fuel_type != current_record.fuel_type THEN
        updates := updates || format('fuel_type = %L', p_fuel_type);
    END IF;
    
    IF p_engine_capacity IS NOT NULL AND p_engine_capacity != current_record.engine_capacity THEN
        updates := updates || format('engine_capacity = %L', p_engine_capacity);
    END IF;
    
    IF p_transmission_type IS NOT NULL AND p_transmission_type != current_record.transmission_type THEN
        updates := updates || format('transmission_type = %L', p_transmission_type);
    END IF;
    
    -- Если нечего обновлять
    IF array_length(updates, 1) IS NULL THEN
        RETURN 'Нет изменений для автомобиля с ID ' || p_car_id;
    END IF;
    
    -- Формируем и выполняем динамический запрос
    update_query := 'UPDATE public.car SET ' || array_to_string(updates, ', ') || 
                   ' WHERE car_id = ' || p_car_id;
    
    EXECUTE update_query;
    
    -- Проверяем результат обновления
    IF FOUND THEN
        result_message := 'Данные автомобиля с ID ' || p_car_id || ' успешно обновлены';
    ELSE
        result_message := 'Не удалось обновить данные автомобиля с ID ' || p_car_id;
    END IF;
    
    RETURN result_message;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при обновлении автомобиля: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_garage(p_old_car_id integer, p_new_car_id integer DEFAULT NULL::integer, p_cars character varying DEFAULT NULL::character varying)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    update_count INT;
BEGIN
    -- Проверяем существование записи
    IF NOT EXISTS (SELECT 1 FROM public.garage WHERE car_id = p_old_car_id) THEN
        RETURN 'Ошибка: запись для car_id ' || p_old_car_id || ' не найдена';
    END IF;
    
    -- Проверяем, не занят ли новый car_id
    IF p_new_car_id IS NOT NULL AND p_new_car_id != p_old_car_id THEN
        IF EXISTS (SELECT 1 FROM public.garage WHERE car_id = p_new_car_id) THEN
            RETURN 'Ошибка: car_id ' || p_new_car_id || ' уже существует';
        END IF;
        
        -- Проверяем, существует ли автомобиль с таким ID
        IF NOT EXISTS (SELECT 1 FROM public.car WHERE car_id = p_new_car_id) THEN
            RETURN 'Ошибка: автомобиль с ID ' || p_new_car_id || ' не существует';
        END IF;
    END IF;
    
    -- Обновляем данные
    UPDATE public.garage
    SET 
        car_id = COALESCE(p_new_car_id, car_id),
        cars = COALESCE(p_cars, cars)
    WHERE car_id = p_old_car_id;
    
    -- Получаем количество обновленных строк
    GET DIAGNOSTICS update_count = ROW_COUNT;
    
    IF update_count > 0 THEN
        RETURN 'Данные успешно обновлены. Новый car_id: ' || 
               COALESCE(p_new_car_id, p_old_car_id);
    ELSE
        RETURN 'Нет изменений для car_id ' || p_old_car_id;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при обновлении: ' || SQLERRM;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_service_history(p_old_car_id integer, p_new_car_id integer DEFAULT NULL::integer, p_motor_oil character varying DEFAULT NULL::character varying, p_air_filter character varying DEFAULT NULL::character varying, p_transmission_oil character varying DEFAULT NULL::character varying, p_cabin_filter character varying DEFAULT NULL::character varying, p_oil_filter character varying DEFAULT NULL::character varying, p_fuel_filter character varying DEFAULT NULL::character varying, p_mileage character varying DEFAULT NULL::character varying)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
DECLARE
    update_count INT;
    v_car_exists BOOLEAN;
BEGIN
    -- 1. Проверяем существование исходной записи
    IF NOT EXISTS (SELECT 1 FROM public.service_history WHERE car_id = p_old_car_id) THEN
        RETURN 'Ошибка: запись с car_id ' || p_old_car_id || ' не найдена';
    END IF;
    
    -- 2. Если указан новый car_id, выполняем проверки
    IF p_new_car_id IS NOT NULL AND p_new_car_id != p_old_car_id THEN
        -- Проверяем существование нового автомобиля
        SELECT EXISTS (SELECT 1 FROM public.car WHERE car_id = p_new_car_id) 
        INTO v_car_exists;
        
        IF NOT v_car_exists THEN
            RETURN 'Ошибка: автомобиль с ID ' || p_new_car_id || ' не существует';
        END IF;
        
        -- Проверяем уникальность нового car_id в service_history
        IF EXISTS (SELECT 1 FROM public.service_history WHERE car_id = p_new_car_id) THEN
            RETURN 'Ошибка: запись с car_id ' || p_new_car_id || ' уже существует';
        END IF;
    END IF;
    
    -- 3. Выполняем обновление
    UPDATE public.service_history
    SET 
        car_id = COALESCE(p_new_car_id, car_id),
        motor_oil = COALESCE(p_motor_oil, motor_oil),
        air_filter = COALESCE(p_air_filter, air_filter),
        transmission_oil = COALESCE(p_transmission_oil, transmission_oil),
        cabin_filter = COALESCE(p_cabin_filter, cabin_filter),
        oil_filter = COALESCE(p_oil_filter, oil_filter),
        fuel_filter = COALESCE(p_fuel_filter, fuel_filter),
        mileage = COALESCE(p_mileage, mileage)
    WHERE car_id = p_old_car_id;
    
    -- 4. Проверяем результат
    GET DIAGNOSTICS update_count = ROW_COUNT;
    
    IF update_count > 0 THEN
        RETURN 'Данные успешно обновлены. ' ||
               CASE WHEN p_new_car_id IS NOT NULL THEN 
                    'Новый car_id: ' || p_new_car_id 
               ELSE 'car_id не изменен' END;
    ELSE
        RETURN 'Нет изменений для car_id ' || p_old_car_id;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Ошибка при обновлении: ' || SQLERRM;
END;
$function$
;
