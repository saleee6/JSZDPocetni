// Autogenerated from service.template file at 18/03/2021 21:47:35
package com.example.demo.generated.services;

import com.example.demo.generated.interfaces.AuthorInterface;
import com.example.demo.generated.models.Author;
import com.example.demo.generated.repositories.AuthorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class AuthorService implements AuthorInterface {

    @Autowired
    private AuthorRepository authorRepository;

    @Override
    public Author getAuthor(Long id) {
        return authorRepository.getAuthorById(id);
    }

    @Override
    public ArrayList<Author> getAllAuthors() {
        return (ArrayList<Author>)authorRepository.findAll();
    }

    @Override
    public Author storeAuthor(Author author) {
        return authorRepository.save(author);
    }

    @Override
    public void deleteAuthor(Long id) {
        Author author = authorRepository.getAuthorById(id);
        authorRepository.delete(author);
    }
}