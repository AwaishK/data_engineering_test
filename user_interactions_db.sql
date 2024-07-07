PGDMP                       |           users    16.3    16.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16398    users    DATABASE     g   CREATE DATABASE users WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE users;
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false                       0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    16399    interactions    TABLE     q   CREATE TABLE public.interactions (
    user_id integer,
    product_id integer,
    interaction_count integer
);
     DROP TABLE public.interactions;
       public         heap    postgres    false    4            �            1259    16411    user_interactions_raw    TABLE     �   CREATE TABLE public.user_interactions_raw (
    interaction_id integer NOT NULL,
    user_id integer NOT NULL,
    product_id integer NOT NULL,
    action character varying(500),
    "timestamp" timestamp without time zone
);
 )   DROP TABLE public.user_interactions_raw;
       public         heap    postgres    false    4                      0    16399    interactions 
   TABLE DATA           N   COPY public.interactions (user_id, product_id, interaction_count) FROM stdin;
    public          postgres    false    215          	          0    16411    user_interactions_raw 
   TABLE DATA           i   COPY public.user_interactions_raw (interaction_id, user_id, product_id, action, "timestamp") FROM stdin;
    public          postgres    false    216   B       w           2606    16417 1   user_interactions_raw pk_interaction_user_product 
   CONSTRAINT     �   ALTER TABLE ONLY public.user_interactions_raw
    ADD CONSTRAINT pk_interaction_user_product PRIMARY KEY (interaction_id, user_id, product_id);
 [   ALTER TABLE ONLY public.user_interactions_raw DROP CONSTRAINT pk_interaction_user_product;
       public            postgres    false    216    216    216            x           1259    16418    user_interactions_per_day    INDEX     b   CREATE INDEX user_interactions_per_day ON public.user_interactions_raw USING btree ("timestamp");
 -   DROP INDEX public.user_interactions_per_day;
       public            postgres    false    216               $   x�3�4�4�2�4�4�2����9��"��c���� ��3      	   �   x�3�4����lN##]C R00�#.#$�?.c ǈ3#�,��������Bޔd`�\��!i�,JML��/J�Gv�����
J��3�SJ�J,�+1B2Œ���j�b��Xܱ��1z\\\ ��A�     